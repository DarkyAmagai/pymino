from threading import Thread as threadIt
from json import loads
from time import sleep
from typing import Optional
import websocket

from .ext.EventHandler import EventHandler
from .ext.context import Context
from .ext.objects import Message
from .ext.http_client import *

class WSClient(EventHandler, Context):
    """
    `WSClient` is a class that handles the websocket.

    `**Example**`
    ```python
    from pymino import Client, WSClient

    client = Client("email", "password")
    ws = WSClient(client)
    ws.connect()
    ```

    `**Parameters**`
    - `client` - The client to use.
    - `debug` - Whether to print debug messages or not. Defaults to `False`.

    """

    def __init__(self, client, debug: bool=True):
        super().__init__()
        self.client = client
        self.debug = debug
        self.sid: Optional[str] = None

        self._ws: Optional[websocket.WebSocket] = None
        self.threads = []
        threadIt(target=self.start_threads).start()


    def start_threads(self):
        """
        `start_threads` start threads in the background.

        `**Example**` `>>> WSClient.start_threads()`

        """
        while True:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)
                    thread.start()
            sleep(0.1)


    def fetch_ws_url(self):
        """
        `fetch_ws_url` is a function that fetches the websocket url.

        `**Example**` `>>> WSClient.fetch_ws_url()`

        """
        self.ws_url=get(f"https://aminoapps.com/api/chat/web-socket-url", headers=self.headers).json()['result']['url']

    def connect(self):
        """
        `connect` is a function that runs the websocket.

        `**Example**` `>>> WSClient.connect()`

        """

        self.sid = self.sid


        self.headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-G975F Build/QP1A.190711.020)",
            "cookie": f"sid={self.sid}"
        }
        websocket.enableTrace(self.debug)
        self.fetch_ws_url()

        self.ws = websocket.WebSocketApp(self.ws_url,
                                         on_open=self._on_ws_open,
                                         on_message=self._on_ws_message,
                                         on_error=self._on_ws_error,
                                         on_close=self._on_ws_close)

        threadIt(target=self.ws.run_forever).start()
        self.emit("ready")
        

    def _on_ws_message(self, ws: websocket.WebSocket, message: dict):
        """
        `_on_ws_message` is a function that handles the websocket message event.

        `**Example**` `>>> WSClient._on_ws_message()`

        """
        message: Message = Message(loads(message))

        if message.type == 0:

            if message.content.startswith(self.command_prefix):
                    command = message.content.split(" ")[0][1:]
                    if command in self._commands:
                        self.threads.append(threadIt(target=self._commands[command](Context(message))))

            self.threads.append(threadIt(target=self._handle_event("text_message", message)))

        elif message.type == 101:
            self.threads.append(threadIt(target=self._handle_event("member_join", message)))

        elif message.type == 102:
            self.threads.append(threadIt(target=self._handle_event("member_leave", message)))


    def _on_ws_error(self, ws: websocket.WebSocket, error: Exception):
        """
        `_on_ws_error` is a function that handles the websocket error event.

        `**Example**` `>>> WSClient._on_ws_error()`

        """
        try:
            self._events["error"](error)
        except KeyError:
            pass

    def _on_ws_close(self, ws: websocket.WebSocket, close_status_code: int, close_msg: str):
        """
        `_on_ws_close` is a function that handles the websocket close event.

        `**Example**` `>>> WSClient._on_ws_close()`

        """
        [ws, close_status_code, close_msg]
        self.run()
        

    def _send_ws_message(self, message: Message):
        """
        `send` is a function that sends a message.

        `**Example**` `>>> WSClient.send(Message())`

        `**Parameters**`
        - `message` - The message to send.

        """
        self.ws.send(dumps(message))

    def stop(self):
        """
        `stop` is a function that stops the websocket.

        `**Example**` `>>> WSClient.stop()`

        """
        [...]

    def _on_ws_open(self, ws: websocket.WebSocket):
        """
        `_on_ws_open` is a function that handles the websocket open event.

        `**Example**` `>>> WSClient._on_ws_open()`

        """
        [ws]