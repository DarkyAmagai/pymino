class Notification:
    def __init__(self, data: dict):
        self.data: dict = data

    @property
    def __parser__(self) -> dict:
        try:
            return self.data.get("o")
        except Exception:
            return self.data
    
    @property
    def payload(self) -> dict:
        """Returns the payload of the notification."""
        return self.__parser__.get("payload")
    
    @property
    def exp(self) -> int:
        """Returns the expiration date of the notification."""
        return self.payload.get("exp")
    
    @property
    def ndcId(self) -> int:
        """Returns the NDC ID of the notification."""
        return self.payload.get("ndcId")
    
    @property
    def comId(self) -> int:
        """Returns the COM ID of the notification."""
        return self.ndcId
    
    @property
    def chatId(self) -> str:
        """Returns the chat ID of the notification."""
        return self.payload.get("tid")
    
    @property
    def aps(self) -> dict:
        """Returns the APS of the notification."""
        return self.payload.get("aps")
    
    @property
    def sound(self) -> str:
        """Returns the sound of the notification."""
        return self.aps.get("sound")
    
    @property
    def alert(self) -> str:
        """Returns the alert of the notification."""
        return self.aps.get("alert")
    
    @property
    def notification_type(self) -> int:
        """Returns the notification type of the notification."""
        return self.payload.get("notifType")
    
    @property
    def id(self) -> str:
        """Returns the ID of the notification."""
        return self.payload.get("id")
    
    def json(self) -> dict:
        """Returns the JSON data of the notification."""
        return self.data