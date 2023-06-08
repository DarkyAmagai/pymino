from typing import Union


class ApiResponse:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    
    @property
    def message(self) -> Union[str, None]:
        """Returns the message of the API response."""
        return self.data.get("api:message")
    
    @property
    def status_code(self) -> Union[int, None]:
        """Returns the status code of the API response."""
        return self.data.get("api:statuscode")
    
    @property
    def duration(self) -> Union[str, None]:
        """Returns the duration of the API response."""
        return self.data.get("api:duration")
    
    @property
    def timestamp(self) -> Union[str, None]:
        """Returns the timestamp of the API response."""
        return self.data.get("api:timestamp")
    
    @property
    def media_value(self) -> Union[str, None]:
        """Returns the media value of the API response."""
        return self.data.get("mediaValue") or self.data.get("result", {}).get("mediaValue")
    
    @property
    def mediaValue(self) -> Union[str, None]:
        #NOTE: This will be removed in the future.
        """Returns the media value of the API response."""
        return self.media_value
    
    def json(self) -> Union[dict, str]:
        """Returns the JSON data of the API response."""
        return self.data
    
    def __repr__(self) -> str:
        """Returns the representation of the API response."""
        return f"<ApiResponse status_code={self.status_code} message={self.message} media_value={self.media_value}>"