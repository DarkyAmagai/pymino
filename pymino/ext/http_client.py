
from json import dumps, loads
from typing import Optional, Union
from uuid import uuid4
from httpx import Client as httpxClient, Response
from .utilities import *

class httpx_handler:
    """
    `httpx_handler` is a class that handles all the requests to the Amino API.

    `**Example**` `>>> httpx_handle(proxies=proxies, debug=debug`)
    

    `**Parameters**`
    - `proxies` - Proxies
    - `debug` - Debug Mode

    `**Returns**`
    - `httpx_handler` - Returns a httpx_handler object

    """
    def __init__(self, proxies: Optional[str]=None, debug: bool=False):
        self.debug = debug
        self.api = "https://service.narvii.com/api/v1"
        self._sid: Optional[str] = None
        self._auid: Optional[str] = None
        self.proxies: str = proxies
        self.session: httpxClient = httpxClient(proxies=self.proxies)

    @property
    def sid(self) -> str: 
        """
        `sid` is a property that returns the session id.
        
        `**Example**` `>>> httpx_handler.sid`
        
        `**Returns**`
        - `str` - Returns the session id.

        """
        return self._sid

    @sid.setter
    def sid(self, value: str):
        """
        `sid` is a property that sets the session id.

        `**Example**` `>>> httpx_handler.sid = value`
        
        `**Parameters**`
        - `value` - The session id.

        """
        self._sid = value

    @property
    def auid(self) -> str:
        """
        `auid` is a property that returns the auid.

        `**Example**` `>>> httpx_handler.auid`

        `**Returns**`
        - `str` - Returns the auid.

        """
        return self._auid

    @auid.setter
    def auid(self, value: str):
        """
        `auid` is a property that sets the auid.

        `**Example**` `>>> httpx_handler.auid = value`
        
        `**Parameters**`
        - `value` - The auid.

        """
        self._auid = value

    def fetch_headers(self, data: Optional[Union[str, bytes, dict]]=None, type: Optional[str]=None) -> dict:
        """
        `fetch_headers` is a method that returns the headers.
        
        `**Example**` `>>> httpx_handler.fetch_headers()`
        
        `**Parameters**`
        - `data` - The data to send. (Optional)
        
        `**Returns**`
        - `dict` - Returns the headers.
        
        """
        headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
            "accept-language": "en-US",
            "content-type": "application/json; charset=utf-8",
            "host": "service.narvii.com",
            "accept-encoding": "gzip",
            "connection": "Upgrade",
            "ndcdeviceid": generate_device_id(),
            "smdeviceid": str(uuid4()),
            }
        if self.sid is not None: headers["ndcauth"]=f"sid={self.sid}"
        if self.auid is not None: headers["auid"]=self.auid

        if data is not None:
            if type is None:
                data=dumps(data)
            else:
                headers["content-type"] = type
            
            headers["content-length"]=str(len(data))
            headers["ndc-msg-sig"]=generate_signature(data)

        return headers
        
    def send(self, method: str, url: str, data=None, type=None) -> Response:
        """
        `send` is a method that sends a request to the Amino API.
        
        `**Example**` `>>> httpx_handler.send(method, url, data)`
        
        `**Parameters**`
        - `method` - The method to use.
        - `url` - The url to send the request to.
        
        `**Returns**`
        - `Response` - Returns the response.
        
        """
        return self.session.request(method, url, headers=self.fetch_headers(data, type), data=dumps(data) if type is None else data)

    def handler(self, method: str, endpoint: str, data: dict=None, type: str=None) -> dict:
        """
        `handler` is a method that handles all the requests to the Amino API.

        `**Example**` `>>> httpx_handler.handler(method, endpoint, data)`
        
        `**Parameters**`
        - `method` - The method to use.
        - `endpoint` - The endpoint to send the request to.
        - `data` - The data to send. (Optional)
        - `type` - The type of data to send. (Optional)
        
        `**Returns**`
        - `dict` - Returns the response.
        
        """
        url = self.api + endpoint

        response = self.send(method, url, data, type)

        if response.status_code != 200:
            if endpoint.endswith(("/g/s/account", "/auth/login")):
                if self.debug: print(f"{{'status_code': {response.status_code}, 'text': '{response.text}'}}")
                return None
            else:
                raise Exception(f"ERROR: {response.text}")

        if self.debug:
            print(f"{{'method': '{method}', 'status_code': {response.status_code}, 'url': '{url}'}}")

        return loads(response.text)