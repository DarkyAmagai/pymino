from contextlib import suppress
from colorama import Fore, Style
from typing import Optional, Union, Tuple, Callable
from requests import Session as HTTPClient, Response as HTTPResponse

from .generate import *
from ..entities import *

if orjson_exists():
    from orjson import loads, dumps
else:
    from json import loads, dumps

from requests.exceptions import (
            ConnectionError,
            ReadTimeout,
            SSLError,
            ProxyError,
            ConnectTimeout
        )

class RequestHandler:
    """
    `RequestHandler` - A class that handles all requests

    `**Parameters**``
    - `bot` - The main bot class.
    - `session` - The session to use for requests.
    - `proxy` - The proxy to use for requests.

    """
    def __init__(self, bot, session: HTTPClient, proxy: Optional[str] = None) -> None:
        self.bot            = bot
        self.sid:           Optional[str] = None
        self.userId:        Optional[str] = None
        self.session:       HTTPClient = session
        self.orjson:        bool = orjson_exists()
        self.proxy:         dict = {"http": proxy,"https": proxy} if proxy is not None else None

    def service_url(self, url: str) -> str:
        """
        `service_url` - Appends the endpoint to the service url
        
        `**Parameters**``
        - `url` - The endpoint to append to the service url.
        
        `**Returns**``
        - `str` - The service url.
        
        """
        return f"http://service.aminoapps.com/api/v1{url}"
    
    def service_headers(self) -> dict:
        """Returns the service headers"""
        return {
            "NDCLANG": "en",
            "ACCEPT-LANGUAGE": "en-US",
            "USER-AGENT": "Apple iPhone13,4 iOS v15.6.1 Main/3.12.9",
            "HOST": "service.aminoapps.com",
            "CONNECTION": "Keep-Alive",
            "ACCEPT-ENCODING": "gzip, deflate, br",
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.userId
            }

    def fetch_request(self, method: str) -> Callable:
        """
        `fetch_request` - Returns the request method
        
        `**Parameters**``
        - `method` - The request method to return.
        
        `**Returns**``
        - `Callable` - The request method.
        
        """

        request_methods = {
            "GET": self.session.get,
            "POST": self.session.post,
            "DELETE": self.session.delete,
            }
        return request_methods[method]

    def handler(
        self,
        method: str,
        url: str,
        data: Union[dict, bytes, None] = None,
        content_type: Optional[str] = None
    ) -> dict:
        """
        `handler` - Handles all requests
        
        `**Parameters**``
        - `method` - The request method to use.
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `content_type` - The content type of the data.
        
        `**Returns**``
        - `dict` - The response from the request.
        
        """

        url, headers, data = self.service_handler(url, data, content_type)
        if all([method=="POST", data is None]):
            headers["CONTENT-TYPE"] = "application/octet-stream"
        
        try:
            response: HTTPResponse = self.fetch_request(method)(
                url, data=data, headers=headers, proxies=self.proxy
            )
        except (
            ConnectionError,
            ReadTimeout,
            SSLError,
            ProxyError,
            ConnectTimeout,
        ):
            self.handler(method, url, data, content_type)

        self.print_response(response)
        return self.handle_response(response)

    def service_handler(
        self,
        url: str,
        data: Union[dict, bytes, None] = None,
        content_type: Optional[str] = None
    ) -> Tuple[str, dict, Union[dict, bytes, None]]:
        """
        `service_handler` - Signs the request and returns the service url, headers and data

        `**Parameters**``
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `content_type` - The content type of the data.
        
        `**Returns**``
        - `Tuple[str, dict, Union[dict, bytes, None]]` - The service url, headers and data.

        """

        service_url = self.service_url(url)
        
        headers = {"NDCDEVICEID": device_id(), **self.service_headers()}

        if data or content_type:
            headers, data = self.fetch_signature(data, headers, content_type)

        return service_url, headers, self.ensure_utf8(data)

    def ensure_utf8(self, data: Union[dict, bytes, None]) -> Union[dict, bytes, None]:
        """
        `ensure_utf8` - Ensures the data is utf-8 encoded
        
        `**Parameters**``
        - `data` - The data to encode.
        
        `**Returns**``
        - `Union[dict, bytes, None]` - The encoded data.
        
        """

        if data is None: return data

        def handle_dict(data: dict):
            return {key: self.ensure_utf8(value) for key, value in data.items()}

        def handle_str(data: str):
            return data.encode("utf-8")

        handlers = {
            dict: handle_dict,
            str: handle_str
        }

        return handlers.get(type(data), lambda x: x)(data)

    def fetch_signature(
        self,
        data: Union[dict, bytes, None],
        headers: dict,
        content_type: str = None
    ) -> Tuple[dict, Union[dict, bytes, None]]:
        """
        `fetch_signature` - Fetches the signature and returns the data and updated headers

        `**Parameters**``
        - `data` - The data to send with the request.
        - `headers` - The headers to send with the request.
        - `content_type` - The content type of the data.

        `**Returns**``
        - `Tuple[dict, Union[dict, bytes, None]]` - The headers and data.

        """

        if not isinstance(data, bytes):
            data = dumps(data).decode("utf-8") if self.orjson else dumps(data)

        headers.update({
            "CONTENT-LENGTH": f"{len(data)}",
            "CONTENT-TYPE": content_type or "application/json; charset=utf-8",
            "NDC-MSG-SIG": (
                generate_signature(data)
            )
        })
        return headers, data

    def handle_response(self, response: HTTPResponse) -> dict:
        """
        `handle_response` - Checks the response and returns the response data if successful

        `**Parameters**``
        - `response` - The response to check.

        `**Returns**``
        - `dict` - The response data.

        """
        if response.status_code != 200:
            
            if response.status_code == 403:
                raise ForbiddenException
            
            with suppress(Exception):
                if loads(response.text).get("api:statuscode") == 105:
                    return self.bot.run(self.email, self.password)

            raise APIException(response.text)

        return loads(response.text)

    def print_response(self, response: HTTPResponse) -> None:
        """
        `print_response` - Prints the response if debug is enabled

        `**Parameters**``
        - `response` - The response to print.

        """
        if self.bot.debug:
            if response.status_code != 200:
                color = Fore.RED
            else:
                color = {"GET": Fore.GREEN, "POST": Fore.YELLOW, "DELETE": Fore.MAGENTA}.get(response.request.method, Fore.RED)

            print(f"{color}{Style.BRIGHT}{response.request.method}{Style.RESET_ALL} - {response.url}")