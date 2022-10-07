from .generate import *
from .context import EventHandler

class WSClient(EventHandler):
    """
    `WSClient` is a class that handles the websocket.
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
        """Starts the threads."""
        while True:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)
                    thread.start()
            sleep(0.1)

    def fetch_ws_url(self):
        """Fetches the websocket url."""
        ws_url = get(f"https://aminoapps.com/api/chat/web-socket-url", headers=self.headers)

        if ws_url.status_code != 200:
            raise Exception(f"Failed to fetch websocket url.\n{ws_url.text}")
            
        return ws_url.json()['result']['url']


    def connect(self):
        """Connects to the websocket."""
        self.run_forever_thread = Thread(target=self.run_forever)
        self.ws_started_time = int(time())
        self.run_forever_thread.start()

        self.emit("ready")
        return None
        
    def fetch_socket(self):
        """Fetches the websocket url and connects to it. """
        return WebSocketApp(self.fetch_ws_url(), on_open=self._on_ws_open, on_message=self._on_ws_message, on_error=self._on_ws_error, on_close=self._on_ws_close)

    def start_forever(self) -> None:
        """Starts the websocket forever."""

        self.ws = self.fetch_socket()
        
        try:
            for thread in [self.ws_thread, self.run_forever_thread]:
                thread.join()
        except (AttributeError, RuntimeError):
            pass
        self.ws_thread = Thread(target=self.ws.run_forever)
        self.ws_thread.start()

        return None

    def run_forever(self):
        """Runs the websocket forever."""

        self.headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-G975F Build/QP1A.190711.020)", "cookie": f"sid={self.sid}"}
        self.start_forever()
        while True:
            if int(time()) - self.ws_started_time > 420:

                try:
                    if self.ws.sock.connected: self.ws.close()
                except (AttributeError, WebSocketConnectionClosedException):
                    pass

                try:
                    if self.ws_thread.is_alive(): self.ws_thread.join()
                except (AttributeError, RuntimeError): 
                    pass

                self.start_forever()

    def _on_ws_error(self, ws: WebSocket, error: Exception) -> None:
        if self.debug: print(f"Websocket error: {error}")
        try:
            self._events["error"](error)
        except KeyError:
            pass

        return None

    def _on_ws_message(self, ws: WebSocket, message: dict):
        """
        `_on_ws_message` is a function that handles the websocket messages.
        """
        if self.debug: print(f"Websocket received message: {message}")
        raw_message = loads(message)

        message: Message = Message(raw_message)

        if message.userId == self.userId: return 

        if raw_message["t"] == 1000:
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
                    
                    return 400  

        elif raw_message["t"] == 201: pass # TODO: Fetch channel key for agora.

        elif raw_message["t"] == 400:
                self.threads.append(Thread(target=self._handle_event, args=("user_online", message.json)))
                return 200
            
        return 400

    def _on_ws_close(self, ws: WebSocket, close_status_code: int, close_msg: str):
        if self.debug: print(f"Websocket closed with status code {close_status_code} and message {close_msg}")

    def _send_ws_message(self, message: dict):
        if self.debug: print(f"Sending message: {message}")
        return self.ws.send(dumps(message))

    def stop_ws(self):
        if self.debug: print("Stopping websocket...")
        return self.ws.close()

    def _on_ws_open(self, ws: WebSocket):
        if self.debug: print(f"Websocket has been opened.")
        if self.community_id is not None:
            return self._send_ws_message(
                message = {
                    "t": 300,
                    "o": {
                        "id": int(time() * 1000),
                        "topic": f"ndtopic:x{self.community_id}:online-members",
                        "ndcId": self.community_id
                    }})