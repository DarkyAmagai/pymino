from uuid import uuid4
from ujson import loads, dumps
from colorama import Fore, Style
from typing import Optional, Union, Tuple, Callable

from .generate import Generator
from ..entities.handlers import orjson_exists
from requests import Session as Http, Response as HttpResponse

from ..entities import (
    Forbidden,
    BadGateway,
    APIException,
    ServiceUnavailable
    )

from requests.exceptions import (
    ConnectionError,
    ReadTimeout,
    SSLError,
    ProxyError,
    ConnectTimeout
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
    - `generator` - The generator class.    
    - `proxy` - The proxy to use for requests.

    """
    def __init__(
        self,
        bot,
        generator: Generator,
        proxy: Optional[str] = None
        ) -> None:
        self.bot             = bot
        self.generate        = generator
        self.http_handler:   Http = Http()
        self.sid:            Optional[str] = None
        self.userId:         Optional[str] = None
        self.orjson:         bool = orjson_exists()

        self.proxy = {
            "http": proxy,
            "https": proxy
            } if proxy is not None else None

        self.response_map = {
            403: Forbidden,
            502: BadGateway,
            503: ServiceUnavailable
            }

    def service_url(self, url: str) -> str:
        """
        `service_url` - Appends the endpoint to the service url
        
        `**Parameters**``
        - `url` - The endpoint to append to the service url.
        
        `**Returns**``
        - `str` - The service url.
        
        """
        return f"http://service.aminoapps.com/api/v1{url}" if url.startswith("/") else url
    
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
            "GET": self.http_handler.get,
            "POST": self.http_handler.post,
            "DELETE": self.http_handler.delete,
            }
        return request_methods[method]
    
    def send_request(
            self,
            method: str,
            url: str,
            data: Union[dict, bytes, None],
            headers: dict,
            content_type: Optional[str]
        ) -> Tuple[int, str]:
        """
        `send_request` - Sends a request
        
        `**Parameters**``
        - `method` - The request method to use.
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `headers` - The headers to send with the request.
        - `content_type` - The content type of the data.
        
        `**Returns**``
        - `Tuple[int, str]` - The status code and response from the request.
        
        """
        try:
            response: HttpResponse = self.fetch_request(method)(
                url, data=data, headers=headers, proxies=self.proxy
            )
            return response.status_code, response.text
        except (
            ConnectionError,
            ReadTimeout,
            SSLError,
            ProxyError,
            ConnectTimeout,
        ) as e:
            self.bot._log(f"Failed to send request: {e}")
            return self.handler(method, url, data, content_type)

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
        url = self.service_url(url)

        url, headers, binary_data = self.service_handler(url, data, content_type)

        if all([method=="POST", data is None]):
            headers["CONTENT-TYPE"] = "application/octet-stream"

        try:
            status_code, content = self.send_request(
                method, url, binary_data, headers, content_type
            )
        except TypeError: # NOTE: Not sure if this is even needed.
            return self.handler(method, url, data, content_type)

        self.print_response(method=method, url=url, status_code=status_code)

        response = self.handle_response(status_code=status_code, response=content)

        if response is None:
            return self.handler(method, url, data, content_type)
        
        return response

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
        
        headers = {"NDCDEVICEID": self.generate.device_id(), **self.service_headers()}

        if data or content_type:
            headers, data = self.fetch_signature(data, headers, content_type)

        return url, headers, self.ensure_utf8(data)

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
                self.generate.signature(data)
            )
        })
        return headers, data

    def raise_error(self, response: dict) -> None:
        """
        `raise_error` - Raises an error if an error is in the response
        
        `**Parameters**``
        - `response` - The response from the request.
        
        `**Returns**``
        - `None` - Raises an error if the status code is in the response map.
        - `404` - Returns 404 if the status code is 105 and the email and password is set.
        
        """
        if all(
            [
                response.get("api:statuscode", 200) == 105,
                hasattr(self, "email"),
                hasattr(self, "password"),
            ]
        ):
            self.bot.run(self.email, self.password, use_cache=False)
            return 404      
      
        self.bot._log(f"Exception: {response}")
        raise APIException(response)
        
    def handle_response(self, status_code: int, response: str) -> dict:
        """
        `handle_response` - Handles the response and returns the response as a dict
        
        `**Parameters**``
        - `status_code` - The status code of the response.
        - `response` - The response to handle.
        
        `**Returns**``
        - `dict` - The response as a dict.
        
        """
        if status_code in self.response_map:
            raise self.response_map[status_code]

        try:
            response = orjson_loads(response) if self.orjson else loads(response)
        except Exception:
            response = loads(response)

        if status_code != 200:
            check_response = self.raise_error(response)
            if check_response == 404:
                return None

        return response

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
            color = Fore.RED if status_code != 200 else {
                "GET": Fore.BLUE,
                "POST": Fore.GREEN,
                "DELETE": Fore.MAGENTA,
                "LITE": Fore.YELLOW
                }.get(method, Fore.RED)
            print(f"{color}{Style.BRIGHT}{method}{Style.RESET_ALL} - {url}")