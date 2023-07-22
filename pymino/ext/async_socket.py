import aiohttp
import asyncio
from time import time
from random import randint
from typing import Optional
from asyncio.queues import Queue
from colorama import Fore, Style
from urllib.parse import urlencode
from ujson import loads, JSONDecodeError
from contextlib import asynccontextmanager

from .entities import *
from .handle_queue import QueueHandler
from .async_event_handler import AsyncEventHandler
from .dispatcher import AsyncMessageDispatcher

if orjson_exists():
    from orjson import loads as orjson_loads


@asynccontextmanager
async def create_client_session():
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


class AsyncWSClient(AsyncEventHandler):
    def __init__(self):
        super().__init__()
        self.ws:            aiohttp.ClientWebSocketResponse = None
        self.session:       aiohttp.ClientSession = None
        self.tasks:         list = []
        self.pool_size:     int = 10
        self.message_queue: Queue = Queue()
        self._last_pinged:  int = time()
        self.reconnecting:  bool = False   
        self._communities:  set = set()
        self.event_types:   dict =  EventTypes().events
        self.notif_types:   dict =  NotifTypes().notifs
        self.dispatcher:    AsyncMessageDispatcher = AsyncMessageDispatcher()
        self.channel:       Optional[Channel] = None
        self.orjson:        bool = orjson_exists()

        self.dispatcher.register(10, self._handle_notification)
        self.dispatcher.register(201, self._handle_agora_channel)
        self.dispatcher.register(400, self._handle_user_online)
        self.dispatcher.register(1000, self._handle_message)


    async def fetch_ws_url(self) -> str:
        return f"wss://ws{randint(1, 4)}.aminoapps.com"
    
    async def logger(self, message: str) -> None:
        print(f"{Fore.RED}[Websocket]{Style.RESET_ALL} {message}")


    async def websocket_forever(self) -> None:
        async for message in self.ws:
            message_handlers = {
                aiohttp.WSMsgType.TEXT: self._handle_text_message,
                aiohttp.WSMsgType.ERROR: self._handle_error_message,
                aiohttp.WSMsgType.CLOSED: self._handle_closed_message
            }

            if message.type in message_handlers:
                await message_handlers[message.type](message)


    async def _handle_text_message(self, message: aiohttp.WSMessage) -> None:
        try:
            self._last_pinged = time()
            raw_message = orjson_loads(message.data) if self.orjson else loads(message.data)
        except JSONDecodeError:
            raw_message = loads(message.data)

        await self.message_queue.put(raw_message)


    async def _handle_error_message(self, message: aiohttp.WSMessage) -> None:
        await self.logger(f"Websocket error: {message.data}")


    async def _handle_closed_message(self, message: aiohttp.WSMessage) -> None:
        await self.logger(f"Websocket closed: {message.data}")
        await self.reconnect()


    async def start_worker_pool(self):
        workers = [QueueHandler(self.message_queue, self.dispatcher) for _ in range(self.pool_size)]
        worker_tasks = [asyncio.create_task(worker.process_messages()) for worker in workers]
        await asyncio.gather(*worker_tasks)


    async def _ready(self) -> None:
        if "ready" in self._events:
            await self.emit("ready")
        else:
            print(f"{Fore.MAGENTA}Logged in as {self.profile.username} ({self.profile.userId}){Style.RESET_ALL}")


    async def reconnect(self) -> None:
        self.reconnecting = True
        await asyncio.sleep(0)
        await self.run_forever()

        
    async def run_forever(self) -> None:
        if self.session:
            await self.session.close()
            del self.session

        try:
            async with create_client_session() as session:
                self.session = session
                ws_data = f"{self.generate.device_id()}|{int(time() * 1000)}"
                self.ws = await session.ws_connect(
                    url=f"{await self.fetch_ws_url()}/?{urlencode({'signbody': ws_data})}",
                    headers={
                        "NDCDEVICEID": self.generate.device_id(),
                        "NDCAUTH": f"sid={self.sid}",
                        "NDC-MSG-SIG": self.generate.signature(ws_data)
                    }
                )

                if not self.tasks:
                    await asyncio.gather(
                        self._ready(),
                        self.start_worker_pool(),
                        alive_loop(self),
                        self.websocket_forever()
                    )
        except Exception as e:
            await self.logger(f"Error: {e}")
            await asyncio.sleep(5)
            await self.reconnect()
   

    async def _handle_message(self, message: dict) -> None:
        _message: Message = Message(message)

        if self.userId == _message.userId:
            return None

        None if any([_message.ndcId is None, _message.ndcId == 0]) else self._communities.add(_message.ndcId)

        key = self.event_types.get(f"{_message.type}:{_message.mediaType}")
        if key is not None:
            self.loop.create_task(self._handle_event(key, _message))


    async def _handle_notification(self, message: dict) -> None:
        notification: Notification = Notification(message)
        key = self.notif_types.get(notification.notification_type)
        if key != None:
            self.loop.create_task(self._handle_event(key, notification))


    async def _handle_agora_channel(self, message: dict) -> None:
        self.channel: Channel = Channel(message)


    async def _handle_user_online(self, message: dict) -> None:
        self.loop.create_task(self._handle_event("user_online", OnlineMembers(message)))


    async def send_websocket_message(self, message: dict) -> None:
        try:
            return await self.ws.send_json(message)
        except ConnectionResetError:
            await self.reconnect()


    async def stop_websocket(self) -> None:
        return await self.ws.close()


    async def _is_interval_elapsed(self, last_time: float, interval: int = 10) -> bool:
        return time() - last_time >= interval


    async def _send_message(self) -> None:
        await self.send_websocket_message({
            "o":{
                "threadChannelUserInfoList": [],
                "id": randint(1, 100)},
                "t": 116
                })


    async def _activity_status(self) -> None:
        for comId in self._communities:

            if self.online_status:
                try:
                    await self.community.send_active(comId=comId,
                    timers=[{"start": int(time()), "end": int(time()) + 300}]
                    )
                except Exception:
                    self.online_status = False

            await asyncio.sleep(randint(5, 10))