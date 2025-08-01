import logging
import urllib.parse
import uuid
from typing import Any, Optional, Union

import colorama
import requests
import ujson

from pymino.ext import entities, global_client, utilities

__all__ = ("RequestHandler",)

logger = logging.getLogger("pymino")


class RequestHandler:
    """A class that handles all requests"""

    __slots__ = (
        "bot",
        "generate",
        "api_url",
        "http_handler",
        "response_map",
        "email",
        "password",
    )

    def __init__(
        self,
        bot: "global_client.Global",
        generator: utilities.Generator,
    ) -> None:
        self.bot = bot
        self.generate = generator
        self.api_url = "http://service.aminoapps.com/api/v1"
        self.http_handler = requests.Session()
        self.response_map = {
            400: entities.BadRequest,
            403: entities.Forbidden,
            502: entities.BadGateway,
            503: entities.ServiceUnavailable,
        }
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    def service_url(self, url: str) -> str:
        """
        Appends the endpoint to the service url

        `**Parameters**``
        - `url` - The endpoint to append to the service url.

        `**Returns**``
        - `str` - The service url.

        """
        return f"{self.api_url}{url}" if url.startswith("/") else url

    def service_headers(self) -> dict[str, str]:
        """Returns the service headers"""
        headers = {
            "NDCLANG": "en",
            "ACCEPT-LANGUAGE": "en-US",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; com.narvii.amino.master/3.5.35071)",
            "HOST": "service.aminoapps.com",
            "CONNECTION": "Keep-Alive",
            "ACCEPT-ENCODING": "gzip, deflate, br",
            "AUID": str(uuid.uuid4()),
        }
        if self.bot.sid:
            headers["NDCAUTH"] = f"sid={self.bot.sid}"
        if self.bot.userId:
            headers["AUID"] = self.bot.userId
        return headers

    def send_request(
        self,
        method: str,
        url: str,
        data: Optional[Union[dict[str, Any], bytes, str]],
        headers: dict[str, str],
        content_type: Optional[str],
    ) -> tuple[int, str]:
        """
        Sends a request.

        `**Parameters**``
        - `method` - The request method to use.
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `headers` - The headers to send with the request.
        - `content_type` - The content type of the data.

        `**Returns**``
        - `tuple[int, str]` - The status code and response from the request.

        """
        proxies = (
            dict.fromkeys(["http", "https"], self.bot.proxy) if self.bot.proxy else None
        )
        try:
            response = self.http_handler.request(
                method,
                url,
                data=data,
                headers=headers,
                proxies=proxies,
            )
        except requests.RequestException as e:
            logger.debug(f"Failed to send request: {e}")
            return self.send_request(method, url, data, headers, content_type)
        return response.status_code, response.text

    def handler(
        self,
        method: str,
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        data: Optional[Union[dict[str, Any], bytes, str]] = None,
        content_type: Optional[str] = None,
        is_login_required: bool = True,
    ) -> dict[str, Any]:
        """
        Handles all requests.

        `**Parameters**``
        - `method` - The request method to use.
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `content_type` - The content type of the data.
        - `is_login_required` - Whether or not the request requires a login.

        `**Returns**``
        - `dict` - The response from the request.

        """
        url = self.service_url(url)

        if isinstance(params, dict):
            if "?" not in url:
                url += "?"
            elif not url.endswith(("&", "?")):
                url += "&"
            url += urllib.parse.urlencode(params)

        if isinstance(data, dict) and self.bot.userId:
            data.update({"uid": self.bot.userId})

        url, headers, binary_data = self.service_handler(url, data, content_type)

        if method == "POST" and data is None:
            headers["CONTENT-TYPE"] = "application/octet-stream"

        if not is_login_required:
            headers.pop("NDCAUTH", None)
            headers.pop("AUID", None)

        status_code, content = self.send_request(
            method, url, binary_data, headers, content_type
        )

        self.print_response(method=method, url=url, status_code=status_code)

        response = self.handle_response(status_code=status_code, response=content)

        if response is None:
            response = self.handler(method, url, data=data, content_type=content_type)

        return response

    def service_handler(
        self,
        url: str,
        data: Optional[Union[dict[str, Any], bytes, str]] = None,
        content_type: Optional[str] = None,
    ) -> tuple[str, dict[str, Any], Optional[bytes]]:
        """
        Signs the request and returns the service url, headers and data

        `**Parameters**``
        - `url` - The url to send the request to.
        - `data` - The data to send with the request.
        - `content_type` - The content type of the data.

        `**Returns**``
        - `tuple[str, dict, Union[dict, bytes, None]]` - The service url, headers and data.

        """
        headers = self.service_headers()
        headers.update({"NDCDEVICEID": self.generate.device_id()})
        if data:
            headers, data = self.fetch_signature(data, headers, content_type)
        else:
            data = None
        return url, headers, data

    def fetch_signature(
        self,
        data: Union[dict[str, Any], bytes, str],
        headers: dict[str, str],
        content_type: Optional[str] = None,
    ) -> tuple[dict[str, str], bytes]:
        """Fetches the signature and returns the data and updated headers.

        `**Parameters**``
        - `data` - The data to send with the request.
        - `headers` - The headers to send with the request.
        - `content_type` - The content type of the data.

        `**Returns**``
        - `tuple[dict, bytes]` - The headers and data.

        """
        if isinstance(data, dict):
            data = ujson.dumps(data)

        if not isinstance(data, bytes):
            data = data.encode("utf-8")

        headers.update(
            {
                "CONTENT-LENGTH": str(len(data)),
                "CONTENT-TYPE": content_type or "application/json; charset=utf-8",
                "NDC-MSG-SIG": self.generate.signature(data),
            }
        )

        if self.bot.userId:
            headers["NDC-MESSAGE-SIGNATURE"] = self.generate.ndc_message_signature(
                data, self.bot.userId
            )

        return headers, data

    def raise_error(self, response: dict[str, Any]) -> None:
        """
        Raises an error if an error is in the response

        `**Parameters**``
        - `response` - The response from the request.

        `**Returns**``
        - `None` - Raises an error if the status code is in the response map.
        - `404` - Returns 404 if the status code is 105 and the email and password is set.

        """
        if (
            response.get("api:statuscode", 200) == 105
            and self.email
            and self.password
            and self.bot.sid
            and entities.SID(self.bot.sid).expired
        ):
            self.bot.run(self.email, self.password, use_cache=False)
            return None

        logger.debug(f"Exception: {response}")
        entities.APIException(response)

    def handle_response(
        self,
        status_code: int,
        response: str,
    ) -> Optional[dict[str, Any]]:
        """
        Handles the response and returns the response as a dict.

        `**Parameters**``
        - `status_code` - The status code of the response.
        - `response` - The response to handle.

        `**Returns**``
        - `dict` - The response as a dict.

        """
        if status_code in self.response_map:
            raise self.response_map[status_code]
        data = ujson.loads(response)
        if status_code != 200:
            self.raise_error(data)
            data = None

        return data

    def print_response(self, method: str, url: str, status_code: int) -> None:
        """
        Prints the response if debug is enabled.

        `**Parameters**``
        - `method` - The request method used.
        - `url` - The url the request was sent to.
        - `status_code` - The status code of the response.
        - `response` - The response to print.

        """
        if not self.bot.debug:
            return
        color = (
            colorama.Fore.RED
            if status_code != 200
            else {
                "GET": colorama.Fore.BLUE,
                "POST": colorama.Fore.GREEN,
                "DELETE": colorama.Fore.MAGENTA,
                "LITE": colorama.Fore.YELLOW,
            }.get(method, colorama.Fore.RED)
        )
        print(
            f"{color}{colorama.Style.BRIGHT}{method}{colorama.Style.RESET_ALL} - {url}"
        )
