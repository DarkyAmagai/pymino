from uuid import uuid4
from ujson import loads, dumps
from contextlib import suppress
from colorama import Fore, Style
from httplib2 import Http as Http2
from typing import Optional, Union, Tuple, Callable

from ..entities.handlers import orjson_exists
from .generate import device_id, generate_signature

from requests import (
    Session as Http, Response as HttpResponse
    )
from ..entities import (
    Forbidden, BadGateway, APIException, ServiceUnavailable
    )
from requests.exceptions import (
    ConnectionError, ReadTimeout, SSLError, ProxyError, ConnectTimeout
    )

if orjson_exists():
    from orjson import (
        loads as orjson_loads,
        dumps as orjson_dumps
        )

class RequestHandler:
    """
    `RequestHandler` - A class that handles all requests

    `**Parameters**``
    - `bot` - The main bot class.
    - `proxy` - The proxy to use for requests.

    """
    def __init__(self, bot, proxy: Optional[str] = None):
        self.bot            = bot
        self._handler:      Http2 = Http2()           
        self.proxy_handler: Http = Http()
        self.sid:           Optional[str] = None
        self.userId:        Optional[str] = None
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
            "AUID": self.userId or str(uuid4())
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
            "GET": self.proxy_handler.get,
            "POST": self.proxy_handler.post,
            "DELETE": self.proxy_handler.delete,
            }
        return request_methods[method]
    
    def run_proxy(
            self,
            method: str,
            url: str,
            data: Union[dict, bytes, None],
            headers: dict,
            content_type: Optional[str]
        ) -> Union[int, str]:
        """
        `run_proxy` - Runs the request with a proxy
        
        `**Parameters**``
        - `method` - The request method to use.
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `headers` - The headers to send with the request.
        - `content_type` - The content type of the data.
        
        `**Returns**``
        - `Union[int, str]` - The status code and response from the request.
        
        """
        try:
            response: HttpResponse = self.fetch_request(method)(
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

        return response.status_code, response.text

    def run_without(
            self,
            method: str,
            url: str,
            data: Union[dict, bytes, None],
            headers: dict,
            content_type: Optional[str]
        ) -> Union[int, str]:
        """
        `run_without` - Runs the request without a proxy
        
        `**Parameters**``
        - `method` - The request method to use.
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `headers` - The headers to send with the request.
        - `content_type` - The content type of the data.
        
        `**Returns**``
        - `Union[int, str]` - The status code and response from the request.
        
        """
        try:
            response, content = self._handler.request(
                url,
                method=method,
                body=data,
                headers=headers
            )
        except (Exception):
            self.handler(method, url, data, content_type)

        return response.status, content
        
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
        
        proxy_map = {True: self.run_proxy, False: self.run_without}

        status_code, content = proxy_map[self.proxy is not None](
            method, url, data, headers, content_type
        )

        self.print_response(method=method, url=url, status_code=status_code)
        return self.handle_response(status_code=status_code, response=content)

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
            data = orjson_dumps(data).decode("utf-8") if self.orjson else dumps(data)

        headers.update({
            "CONTENT-LENGTH": f"{len(data)}",
            "CONTENT-TYPE": content_type or "application/json; charset=utf-8",
            "NDC-MSG-SIG": (
                generate_signature(data)
            )
        })
        return headers, data

    def handle_response(self, status_code: int, response: bytes) -> dict:
        """
        `handle_response` - Checks the response and returns the response data if successful

        `**Parameters**``
        - `response` - The response to check.

        `**Returns**``
        - `dict` - The response data.

        """
        response_map = {403: Forbidden, 502: BadGateway, 503: ServiceUnavailable}

        with suppress(Exception):

            if status_code != 200:
                
                if status_code in response_map:
                    raise response_map[status_code]
                
                if dict(loads(response)).get("api:statuscode") == 105:
                    return self.bot.run(self.email, self.password)

                raise APIException(response)
        
            return orjson_loads(response) if self.orjson else loads(response)

        return loads(response)

    def print_response(self, method: str, url: str, status_code: int):
        """
        `print_response` - Prints the response if debug is enabled

        `**Parameters**``
        - `method` - The request method used.
        - `url` - The url the request was sent to.
        - `status_code` - The status code of the response.
        - `response` - The response to print.

        """
        if self.bot.debug:
            color = Fore.RED if status_code != 200 else {"GET": Fore.GREEN, "POST": Fore.YELLOW, "DELETE": Fore.MAGENTA}.get(method, Fore.RED)
            print(f"{color}{Style.BRIGHT}{method}{Style.RESET_ALL} - {url}")