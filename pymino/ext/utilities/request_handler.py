from .generate import *

class RequestHandler:
    """A class that handles all requests"""
    def __init__(self, bot, session: HTTPClient, proxy: Optional[str] = None):
        self.bot            = bot
        self.session:       HTTPClient = session
        self.proxy:         Optional[str] = {"http": proxy, "https": proxy} if proxy is not None else None
        self.headers:       dict = {
                            "NDCLANG": "en",
                            "ACCEPT-LANGUAGE": "en-US",
                            "USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/LYZ28N; com.narvii.amino.master/3.5.34654)",
                            "HOST": "service.aminoapps.com",
                            "CONNECTION": "Keep-Alive",
                            "ACCEPT-ENCODING": "gzip"
                            }

    def handler(self, method: str, url: str, data: Union[dict, bytes, None] = None, content_type: Optional[str] = None):
        url = f"https://service.aminoapps.com/api/v1{url}"

        headers = {**self.headers, "NDCDEVICEID": device_id()}
        request_methods = {"GET": self.session.get, "POST": self.session.post, "DELETE": self.session.delete}

        if any([data, content_type]):
            data = data if isinstance(data, bytes) else dumps(data)
            headers.update({
                "CONTENT-LENGTH": f"{len(data)}",
                "NDC-MSG-SIG": signature(data),
                "CONTENT-TYPE": content_type if content_type is not None else "application/json; charset=utf-8"
                })
        else:
            headers["CONTENT-TYPE"] = "application/json; charset=utf-8"
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
