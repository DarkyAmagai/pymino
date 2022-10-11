from .utilities.generate import *
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

    def connect(self):
        """Connects to the websocket."""
        self.started = False
        self.run_forever_thread = Thread(target=self.run_forever)
        self.ws_started_time = int(time())
        self.run_forever_thread.start()

        self.emit("ready")
        return None

    def run_forever(self):
        """Runs the websocket forever."""
        query = f"{device_id()}|{int(time() * 1000)}"
        self.headers = {
            "USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/LYZ28N; com.narvii.amino.master/3.5.34654)",
            "NDCDEVICEID": device_id(),
            "AUID": self.userId,
            "NDC-MSG-SIG": signature(query),
            "NDCAUTH": f"sid={self.sid}",
            "NDCLANG": "en",
            "ACCEPT-LANGUAGE": "en-US",
            "UPGRADE": "websocket",
            "CONNECTION": "Upgrade"
        }
        self.ws = WebSocketApp(f"wss://ws{randint(1, 4)}.aminoapps.com/?signbody={query.replace('|', '%7C')}", header=self.headers, on_open=self._on_ws_open, on_message=self._on_ws_message, on_error=self._on_ws_error, on_close=self._on_ws_close)
        Thread(target=self._keep_alive).start()
        self.ws.run_forever()

    def _keep_alive(self):
        if self.debug: print("Starting keep alive thread...")
        wait(5) # Wait for the websocket to connect.
        while True:
            self._send_ws_message({
                "o":{
                    "threadChannelUserInfoList": [],
                    "id": randint(1, 100)},
                    "t": 116
                    })
            wait(30)

    def _on_ws_error(self, ws: WebSocket, error: Exception) -> None:
        if self.debug: print(f"Websocket error: {error}")
        try: self._events["error"](error)
        except KeyError: pass

        return None

    def _on_ws_message(self, ws: WebSocket, message: dict):
        """
        `_on_ws_message` is a function that handles the websocket messages.
        """
        
        if self.debug: print(f"Websocket received message: {message}")

        raw_message = loads(message)
        message: Message = Message(raw_message)

        if message.userId == self.userId: return None

        if raw_message["t"] == 1000:
            def fetch_key():
                message_type = f"{message.type}:{message.mediaType}"
                for key, value in EventTypes.__dict__.items():
                    if value == message_type:
                        return key
                return None

            key = fetch_key()
            if key is not None:
                if any([message.content == None or not message.content.startswith(self.command_prefix)]):
                    return Thread(target=self._handle_event, args=(key, message)).start()
                else:
                    return Thread(target=self._handle_command(message.json)).start()
            else:
                return None

        elif raw_message["t"] == 201: pass # TODO: Fetch channel key for agora.

        elif raw_message["t"] == 400:
                return Thread(target=self._handle_event, args=("user_online", message.json)).start()
            
        return None

    def _on_ws_close(self, ws: WebSocket, close_status_code: int, close_msg: str):
        if self.debug: print(f"Websocket closed with status code {close_status_code} and message {close_msg}")
        if close_status_code == None and close_msg == None:
            self.run_forever()
        return None
        
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