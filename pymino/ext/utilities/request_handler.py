from .generate import *

class RequestHandler:
    """A class that handles all requests"""
    def __init__(self, bot, session: HTTPClient, proxy: Optional[str] = None):
        self.bot            = bot
        self.sid:           Optional[str] = None
        self.userId:        Optional[str] = None
        self.session:       HTTPClient = session
        self.proxy:         Optional[str] = {"http": proxy, "https": proxy} if proxy is not None else None

    @property
    def service_headers(self) -> dict:
        return {
            "NDCLANG": "en",
            "ACCEPT-LANGUAGE": "en-US",
            "USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/LYZ28N; com.narvii.amino.master/3.5.34654)",
            "HOST": "service.aminoapps.com",
            "CONNECTION": "Keep-Alive",
            "ACCEPT-ENCODING": "gzip",
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.userId,
            "CONTENT-TYPE": "application/json; charset=utf-8"
            }

    @property
    def default_headers(self) -> dict:
        return {
            "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36",
            "HOST": "aminoapps.com",
            "X-REQUESTED-WITH": "xmlhttprequest",
            "ACCEPT-ENCODING": "gzip, deflate",
            "COOKIE": f"sid={self.sid}",
            "CONTENT-TYPE": "application/json"
            }

    def service_handler(
        self,
        url: str,
        data: Union[dict, bytes, None] = None,
        content_type: Optional[str] = None
        ) -> Tuple[str, dict, Union[dict, bytes, None]]:
        url = f"https://service.aminoapps.com/api/v1{url}"
        headers = {**self.service_headers, "NDCDEVICEID": device_id()}
        
        if any([data, content_type]):
            data = data if isinstance(data, bytes) else dumps(data)
            headers.update({
                "CONTENT-LENGTH": f"{len(data)}",
                "NDC-MSG-SIG": signature(data), 
                "CONTENT-TYPE": content_type if content_type is not None else "application/json; charset=utf-8"
                })

        return url, headers, data

    def default_handler(
        self,
        url: str,
        data: Union[dict, bytes, None] = None,
        content_type: Optional[str] = None
        ) -> Tuple[str, dict, Union[dict, bytes, None]]:
        headers = self.default_headers

        if any([data, content_type]):
            data = data if isinstance(data, bytes) else dumps(data)
            headers.update({"CONTENT-LENGTH": f"{len(data)}"})
            if content_type is not None:
                data: MultipartEncoder = self.encode_data(data)
                headers.update({"CONTENT-TYPE": data.content_type})

        return url, headers, data

    def encode_data(self, data: bytes) -> MultipartEncoder:
        uuid = str(uuid4())
        return MultipartEncoder(
            fields={
                "qqparentuuid": uuid,
                "qqparentsize": str(len(data)),
                "qquuid": uuid,
                "qqfilename": f"{uuid}.png",
                "qqtotalfilesize": str(len(data)),
                "avatar": (f"{uuid}.gif", data, "image/gif")
                })

    def handler(self, method: str, url: str, data: Union[dict, bytes, None] = None, content_type: Optional[str] = None):

        url, headers, data = self.default_handler(url, data, content_type) if url.startswith("http") else self.service_handler(url, data, content_type)

        request_methods = {"GET": self.session.get, "POST": self.session.post, "DELETE": self.session.delete}

        try:
            response: HTTPResponse = request_methods[method](url, data=data, headers=headers, proxies=self.proxy)
        except (ConnectionError, ReadTimeout, SSLError, ProxyError, ConnectTimeout):
            self.handler(method, url, data, content_type)

        if response.status_code != 200:
            with suppress(Exception):
                response_json: dict = loads(response.text)
                # TODO: Handle exceptions.
                if response_json.get("api:statuscode") == 105: return self.bot.run(self.email, self.password)

            raise Exception(response.text)

        return loads(response.text)