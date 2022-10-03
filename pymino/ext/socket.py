from .generate import *
from .context import EventHandler

class WSClient(EventHandler):
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

    def __init__(self, client, debug: Optional[bool] = False):
        EventHandler.__init__(self)
        self.client = client
        self.debug = debug
        self.sid: Optional[str] = None
        self._ws: Optional[WebSocket] = None
        self.threads = []
        Thread(target=self.start_threads).start()

    def start_threads(self):
        while True:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)
                    thread.start()
            sleep(0.1)

    def fetch_ws_url(self):
        """Fetches the websocket url."""
        self.ws_url=get(f"https://aminoapps.com/api/chat/web-socket-url", headers=self.headers).json()['result']['url']

    def connect(self):
        """Connects to the websocket."""
        self.sid = self.sid
        self.headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-G975F Build/QP1A.190711.020)",
            "cookie": f"sid={self.sid}"
        }

        self.fetch_ws_url()
        self.ws = WebSocketApp(self.ws_url, on_open=self._on_ws_open, on_message=self._on_ws_message, on_error=self._on_ws_error, on_close=self._on_ws_close)

        Thread(target=self.ws.run_forever).start()
        #Thread(target=self._keep_alive).start() #NOTE: This is not needed, but it's here just in case.
        self.emit("ready")
        
    def _on_ws_message(self, ws: WebSocket, message: dict):
        """
        `_on_ws_message` is a function that handles the websocket messages.
        """
        message: Message = Message(loads(message))

        if message.userId == self.userId: return 

        for key, value in EventTypes.__dict__.items():
            if value == f"{message.type}:{message.mediaType}":

                if (message.content == None or not message.content.startswith(self.command_prefix)):
                    self.threads.append(Thread(target=self._handle_event, args=(key, message)))
                    return 200

                elif message.content is not None and message.content.startswith(self.command_prefix):
                    command = message.content.split(" ")[0][len(self.command_prefix):]

                    if command in self._commands:
                        self.threads.append(Thread(target=self._handle_command(message.json)))
                    return 200
                else:
                    return 400         
    
    def _keep_alive(self):
        while True:
            if not self.ws.sock.connected:
                self.ws.close()
                sleep(5)
                self.connect()
            if self.debug:
                print("WebSocket is alive")

    def _on_ws_error(self, ws: WebSocket, error: Exception):
        try: self._events["error"](error)
        except KeyError: pass
    def _on_ws_close(self, ws: WebSocket, close_status_code: int, close_msg: str):
        [ws, close_status_code, close_msg]
        self.connect()
    def _send_ws_message(self, message: Message): self.ws.send(dumps(message))
    def stop(self): self.ws.close()
    def _on_ws_open(self, ws: WebSocket): [ws]
