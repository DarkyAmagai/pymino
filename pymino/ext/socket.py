from random import randint
from typing import Optional
from threading import Thread
from time import sleep as delay
from websocket import (
    WebSocket,
    WebSocketApp,
    WebSocketConnectionClosedException
    )
from .entities import *
from .context import EventHandler
from .utilities.generate import *
from .dispatcher import MessageDispatcher

if orjson_exists():
    from orjson import loads, dumps
else:
    from json import loads, dumps

class WSClient(EventHandler):
    """
    `WSClient` is a class that handles the websocket.

    `**Parameters**`
    - `bot` - The bot client to use.

    """
    def __init__(self, bot):
        self.ws:            WebSocketApp = None
        self.bot            = bot
        self.event_types:   dict =  EventTypes().events
        self.dispatcher:    MessageDispatcher = MessageDispatcher()
        self.channel:       Optional[Channel] = None
        self.orjson:        bool = orjson_exists()
        
        self.dispatcher.register(201, self._handle_agora_channel)
        self.dispatcher.register(400, self._handle_user_online)
        self.dispatcher.register(1000, self._handle_message)
        EventHandler.__init__(self)
        
    def fetch_ws_url(self) -> str:
        return f"wss://ws{randint(1, 4)}.aminoapps.com"

    def connect(self) -> None:
        """Connects to the websocket."""
        self.run_forever()
        return self.emit("ready")

    def run_forever(self) -> None:
        """Runs the websocket forever."""
        ws_data = f"{device_id()}|{int(time() * 1000)}"
        self.ws = WebSocketApp(
            url=f"{self.fetch_ws_url()}/?signbody={ws_data.replace('|', '%7C')}",
            on_open=self.on_websocket_open,
            on_message=self.on_websocket_message,
            on_error=self.on_websocket_error,
            on_close=self.on_websocket_close,
            header={
            "NDCDEVICEID": device_id(),
            "NDCAUTH": f"sid={self.bot.sid}",
            "NDC-MSG-SIG": generate_signature(ws_data)
            })
        return self.start_processes()

    def start_processes(self) -> None:
        """Starts the websocket processes."""
        for process in[self.ws.run_forever, self.heartbeat]:
            Thread(target=process).start()

    def heartbeat(self) -> None:
        """Sends a heartbeat to the websocket."""""
        while True:
            with suppress(WebSocketConnectionClosedException):
                delay(randint(25, 50))
                self.send_websocket_message({
                    "o":{
                        "threadChannelUserInfoList": [],
                        "id": randint(1, 100)},
                        "t": 116
                        })

    def on_websocket_error(self, ws: WebSocket, error: Exception) -> None:
        """Handles websocket errors."""
        with suppress(KeyError):
            self._events["error"](error)

    def on_websocket_message(self, ws: WebSocket, message: dict) -> None:
        """Handles websocket messages."""
        raw_message = loads(message)
        self.dispatcher.handle(raw_message)

    def _handle_message(self, message: dict) -> None:
        """Sends the message to the event handler."""
        message: Message = Message(message)
        if self.userId == message.userId: return None

        key = self.event_types.get(f"{message.type}:{message.mediaType}")
        
        if key != None:
            return Thread(target=self._handle_event, args=(key, message)).start()

    def _handle_agora_channel(self, message: dict) -> None:
        """Sets the agora channel."""
        self.channel: Channel = Channel(message)

    def _handle_user_online(self, message: dict) -> None:
        """Handles user online events."""
        return self._handle_event("user_online", OnlineMembers(message))

    def on_websocket_close(self, ws: WebSocket, close_status_code: int, close_msg: str) -> None:
        """Handles websocket close events."""
        if [close_status_code, close_msg] == [None, None]:
            return self.run_forever() 
        
    def send_websocket_message(self, message: dict) -> None:
        """Sends a websocket message."""
        return self.ws.send(dumps(message).decode() if self.orjson else dumps(message))

    def stop_websocket(self) -> None:
        """Stops the websocket."""
        return self.ws.close()

    def on_websocket_open(self, ws: WebSocket) -> None:
        """Handles websocket open events."""
        if all([self.bot.community_id != None, "user_online" in self._events]):
            return self.send_websocket_message({
                "t": 300,
                "o": {
                    "ndcId": self.bot.community_id,
                    "topic": f"ndtopic:x{self.bot.community_id}:online-members",
                    "id": int(time() * 1000)
                }})