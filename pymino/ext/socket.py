from .utilities.generate import *
from .context import EventHandler

class WSClient(EventHandler):
    """
    `WSClient` is a class that handles the websocket.
    ```

    `**Parameters**`
    - `client` - The bot client to use.

    """
    def __init__(self, client):
        EventHandler.__init__(self)
        self.client = client
        self.channel: Optional[Channel] = None

    def fetch_headers(self, query: str):
        return {
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

    def connect(self):
        """Connects to the websocket."""
        self.run_forever()
        return self.emit("ready")

    def run_forever(self):
        """Runs the websocket forever."""
        query = f"{device_id()}|{int(time() * 1000)}"
        self.ws = WebSocketApp(
            url=f"wss://ws{randint(1, 4)}.aminoapps.com/?{urlencode({'signbody': query})}",
            header=self.fetch_headers(query),
            on_open=self.on_websocket_open,
            on_message=self.on_websocket_message,
            on_error=self.on_websocket_error,
            on_close=self.on_websocket_close
            )
        return self.start_processes()

    def start_processes(self):
        """Starts the websocket processes."""
        for process in[self.ws.run_forever, self.websocket_worker]:
            Thread(target=process).start()
        return None

    def websocket_worker(self):
        """Runs the websocket worker."""
        while True:
            with suppress(WebSocketConnectionClosedException):
                wait(randint(25, 50))
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
        return None

    def on_websocket_message(self, ws: WebSocket, message: dict):
        """Handles websocket messages."""
        raw_message_types = {
            201: self._handle_agora_channel,
            400: self._handle_user_online,
            1000: self._handle_message
            }
        raw_message: dict = loads(message)
        
        return raw_message_types.get(raw_message["t"], lambda x: None)(raw_message)

    def _handle_message(self, message: dict):
        """Sends the message to the event handler."""
        message: Message = Message(message)
        
        if self.userId == message.userId: return None
        key = EventTypes.reverse_dictionary.get(f"{message.type}:{message.mediaType}", None)

        if key != None:
            return Thread(target=self._handle_event, args=(key, message)).start()

        return None

    def _handle_agora_channel(self, message: dict):
        """Sets the agora channel."""
        self.channel: Channel = Channel(message)
        return None

    def _handle_user_online(self, message: dict):
        """Handles user online events."""
        return Thread(target=self._handle_event, args=("user_online", OnlineMembers(message))).start()

    def on_websocket_close(self, ws: WebSocket, close_status_code: int, close_msg: str):
        """Handles websocket close events."""
        if [close_status_code, close_msg] == [None, None]:
            return self.run_forever() 
        return None
        
    def send_websocket_message(self, message: dict):
        """Sends a websocket message."""
        return self.ws.send(dumps(message))

    def stop_websocket(self):
        """Stops the websocket."""
        return self.ws.close()

    def on_websocket_open(self, ws: WebSocket):
        """Handles websocket open events."""
        if all([self.community_id != None, "user_online" in self._events]):
            return self.send_websocket_message({
                "t": 300,
                "o": {
                    "ndcId": self.community_id,
                    "topic": f"ndtopic:x{self.community_id}:online-members",
                    "id": int(time() * 1000)
                }})
        return None