from .utilities.generate import *
from .context import EventHandler

class WSClient(EventHandler):
    """
    `WSClient` is a class that handles the websocket.
    ```

    `**Parameters**`
    - `client` - The client to use.
    """

    def __init__(self, client):
        EventHandler.__init__(self)
        self.client = client
        self.sid: Optional[str] = None
        self._ws: Optional[WebSocket] = None

    def connect(self):
        """Connects to the websocket."""
        Thread(target=self.run_forever).start()
        return self.emit("ready")

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
        self.ws = WebSocketApp(f"wss://ws{randint(1, 4)}.aminoapps.com/?signbody={query.replace('|', '%7C')}", header=self.headers, on_open=self.on_websocket_open, on_message=self.on_websocket_message, on_error=self.on_websocket_error, on_close=self.on_websocket_close)
        Thread(target=self._keep_alive).start()
        return self.ws.run_forever()

    def _keep_alive(self):
        wait(5) # Wait for the websocket to connect.
        while True:
            self.send_websocket_message({
                "o":{
                    "threadChannelUserInfoList": [],
                    "id": randint(1, 100)},
                    "t": 116
                    })
            wait(30)

    def on_websocket_error(self, ws: WebSocket, error: Exception) -> None:
        try: 
            return self._events["error"](error)
        except KeyError:
            return None

    def on_websocket_message(self, ws: WebSocket, message: dict):
        raw_message_types = {
            201: self._handle_agora_channel_key,
            400: self._handle_user_online,
            1000: self._handle_message
        }
        raw_message = loads(message)
        message: Message = Message(raw_message)
        if any([message.author.userId == self.userId, raw_message["t"] not in raw_message_types]):
            return None

        return raw_message_types[raw_message["t"]](message) 

    def _handle_message(self, message: Message):
        key = EventTypes.reverse_dictionary.get(f"{message.type}:{message.mediaType}", None)
        if key != None:
            return Thread(target=self._handle_event, args=(key, message)).start()
        
        return None

    def _handle_agora_channel_key(self, message: Message):
        return None

    def _handle_user_online(self, message: Message):
        return Thread(target=self._handle_event, args=("user_online", message.json)).start()

    def on_websocket_close(self, ws: WebSocket, close_status_code: int, close_msg: str):
        if close_status_code == None and close_msg == None:
            self.run_forever()
        return None
        
    def send_websocket_message(self, message: dict):
        return self.ws.send(dumps(message))

    def stop_websocket(self):
        return self.ws.close()

    def on_websocket_open(self, ws: WebSocket):
        if self.community_id is not None:
            return self.send_websocket_message(
                message = {
                    "t": 300,
                    "o": {
                        "id": int(time() * 1000),
                        "topic": f"ndtopic:x{self.community_id}:online-members",
                        "ndcId": self.community_id
                    }})