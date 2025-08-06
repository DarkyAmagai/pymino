import abc
import logging
import random
import signal
import threading
import time
import urllib.parse
from typing import Any, Optional, Union

import ujson
import websocket

from pymino.ext import context, dispatcher, entities, utilities

__all__ = ("WSClient",)

logger = logging.getLogger("pymino")


class WSClient(context.EventHandler):
    """
    WSClient class that handles websocket events.

    This class extends `EventHandler` class, allowing the bot to use event handler features.

    Attributes:
    ws : WebSocketApp
        The websocket object.
    _communities : set
        A set containing the communities the bot is in.
    dispatcher : MessageDispatcher
        The message dispatcher object.
    channel : Optional[Channel]
        The agora channel.
    orjson : bool
        Whether or not orjson is installed.

    """

    __slots__ = (
        "_communities",
        "_task_runner_active",
        "channel",
        "dispatcher",
        "ws",
    )

    @property
    @abc.abstractmethod
    def community_id(self) -> Optional[int]: ...

    @property
    @abc.abstractmethod
    def generate(self) -> utilities.Generator: ...

    @property
    @abc.abstractmethod
    def proxy(self) -> Optional[str]: ...

    @property
    @abc.abstractmethod
    def userId(self) -> Optional[str]: ...

    @property
    @abc.abstractmethod
    def device_id(self) -> str: ...

    @property
    @abc.abstractmethod
    def sid(self) -> Optional[str]: ...

    def __init__(self) -> None:
        self.ws: Optional[websocket.WebSocket] = None
        self.dispatcher: dispatcher.MessageDispatcher = dispatcher.MessageDispatcher()

        self.dispatcher.register(
            entities.WsMessageTypes.PUSH_NOTIFICATION_DTO, self._handle_notification
        )
        self.dispatcher.register(
            entities.WsMessageTypes.AGORA_TOKEN_RESPONSE, self._handle_agora_channel
        )
        self.dispatcher.register(
            entities.WsMessageTypes.LIVE_LAYER_USER_JOINED_EVENT,
            self._handle_user_online,
        )
        self.dispatcher.register(
            entities.WsMessageTypes.CHAT_MESSAGE_DTO, self._handle_message
        )
        self._communities: set[int] = set()
        self._task_runner_active: bool = False
        self.channel: Optional[entities.Channel] = None

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        super().__init__()

    def fetch_ws_url(self) -> str:
        return f"wss://ws{random.randint(1, 4)}.aminoapps.com/"

    def connect(self) -> None:
        """Connects to the websocket."""
        if not self.sid:
            raise RuntimeError("Cannot connect websocket when the bot is not logged")
        threading.Thread(target=self._run_forever).start()
        while not self.connected:
            time.sleep(1)

    @property
    def connected(self) -> bool:
        return bool(self.ws and self.ws.connected)

    def _run_forever(self) -> None:
        """Runs the websocket forever."""
        if not self.sid:
            return
        if self.connected:
            return
        while self.sid:
            if not self.ws:
                self.ws = websocket.WebSocket()
            if not self.connected:
                logger.debug("Initializing websocket.")
                ws_data = f"{self.device_id}|{int(time.time() * 1000)}"
                url = f"{self.fetch_ws_url()}?" + urllib.parse.urlencode(
                    {"signbody": ws_data}
                )
                kwargs: dict[str, Any] = {
                    "header": {
                        "NDCDEVICEID": self.device_id,
                        "NDCAUTH": f"sid={self.sid}",
                        "NDC-MSG-SIG": self.generate.signature(ws_data),
                    }
                }
                if self.proxy:
                    proxy = urllib.parse.urlparse(self.proxy)
                    kwargs["http_proxy_host"] = proxy.hostname
                    kwargs["http_proxy_port"] = proxy.port
                    kwargs["http_proxy_auth"] = (proxy.username, proxy.password)
                try:
                    self.ws.connect(  # pyright: ignore[reportUnknownMemberType]
                        url, **kwargs
                    )
                except websocket.WebSocketConnectionClosedException:
                    time.sleep(1)
                    logger.debug("Websocket handshake failed.")
                    continue
                self._on_websocket_open()
            try:
                message = self.ws.recv()
            except websocket.WebSocketException as exc:
                self._on_websocket_error(exc)
                self.stop_websocket()
                continue
            self._on_websocket_message(message)
        self.stop_websocket()

    def _on_websocket_error(self, error: Exception) -> None:
        """Handles websocket errors."""
        callback = self._events.get("error")
        if callback:
            threading.Thread(target=callback, args=(error,)).start()

        logger.debug(f"Websocket error: {error}")

    def _on_websocket_message(self, message: Union[bytes, str]) -> None:
        """Receives websocket messages."""
        threading.Thread(target=self._handle_websocket_message, args=(message,)).start()

    def _on_websocket_close(self) -> None:
        """Handles websocket close events."""
        logger.debug(f"Websocket closed unexpectedly.")

    def _on_websocket_open(self) -> None:
        """Handles websocket open events."""
        threading.Thread(target=self._task_runner_loop).start()
        self.emit("ready")
        if self.community_id and "user_online" in self._events:
            self.send_websocket_message(
                {
                    "t": entities.WsMessageTypes.LIVE_LAYER_SUBSCRIBE_REQUEST,
                    "o": {
                        "ndcId": self.community_id,
                        "topic": f"ndtopic:x{self.community_id}:online-members",
                        "id": int(time.monotonic() + random.randint(1, 100)),
                    },
                }
            )

    def _handle_websocket_message(self, message: Union[bytes, str]) -> None:
        """Handles websocket messages."""
        try:
            self.dispatcher.handle(ujson.loads(message))
        except ujson.JSONDecodeError:
            logger.error(f"Unhandled ws message: {message!r}")

    def _handle_message(self, data: dict[str, Any]) -> None:
        """Sends the message to the event handler."""
        message = entities.Message(data)

        if self.userId == message.userId:
            return None
        if message.comId:
            self._communities.add(message.comId)

        key = entities.EVENT_TYPES.get(f"{message.type}:{message.mediaType}")

        if key:
            self._handle_event(key, message)

    def _handle_notification(self, message: dict[str, Any]) -> None:
        """Handles notifications."""
        notification = entities.Notification(message)
        key = entities.NOTIF_TYPES.get(notification.notification_type)
        if key:
            self._handle_event(key, notification)

    def _handle_agora_channel(self, message: dict[str, Any]) -> None:
        """Sets the agora channel."""
        self.channel = entities.Channel(message)

    def _handle_user_online(self, message: dict[str, Any]) -> None:
        self._handle_event("user_online", entities.OnlineMembers(message))

    def send_websocket_message(
        self,
        message: Union[dict[str, Any], bytes, str],
    ) -> None:
        """Sends a websocket message."""
        if not self.ws:
            return None
        if not isinstance(message, (bytes, str)):
            message = ujson.dumps(message)
        self.ws.send(ujson.dumps(message))

    def stop_websocket(self) -> None:
        """Stops the websocket."""
        if self.connected and self.ws:
            self.ws.close()
            logger.debug("Websocket received stop signal.")
        self.ws = None

    def _last_active(self, last_activity_time: float) -> bool:
        """Returns True if the last activity was 5 minutes ago."""
        return time.time() - last_activity_time >= 300

    def _send_ping(self) -> None:
        self.send_websocket_message(
            {
                "o": {
                    "threadChannelUserInfoList": [],
                    "id": random.randint(1, 100),
                },
                "t": entities.WsMessageTypes.CHANNEL_USER_PING_REQUEST,
            }
        )

    def _activity_status(self) -> None:
        """Sets the user's activity status to online."""
        for comId in self._communities:
            if self.online_status:
                try:
                    self.community.send_active(
                        start=int(time.time()),
                        end=int(time.time()) + 300,
                        comId=comId,
                    )
                except Exception:
                    self.online_status = False

            time.sleep(random.randint(5, 10))

    def _task_runner_loop(self) -> None:
        """Handles websocket messages."""
        if self._task_runner_active:
            return
        self._task_runner_active = True
        while self.connected:
            if not self._tasks:
                continue
            task, interval = self._tasks.pop(0)
            threading.Thread(
                target=self._handle_task,
                args=(
                    task,
                    interval,
                ),
            ).start()
