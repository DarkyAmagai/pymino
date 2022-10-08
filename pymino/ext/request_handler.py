from . generate import *

class RequestHandler:
    """
    A class that handles all requests
    """
    def __init__(self, session: Session, debug: Optional[bool] = False):
        self.session = session
        self.debug = debug
        self._responses = []
        self.threads = []
        Thread(target=self.start_threads).start()

    def start_threads(self):
        while True:
            for thread in self.threads:
                if not Thread(thread).is_alive():
                    self.threads.remove(thread)
                    Thread(thread).start()
            sleep(0.1)

    def device_id(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args[0].session.headers.update({"NDCDEVICEID": device_id()})
            if args[0].debug:
                print(f"Device ID: {args[0].session.headers.get('NDCDEVICEID')}")
            return func(*args, **kwargs)
        return wrapper

    @device_id
    def handler(self, method: str, url: str, data: Union[dict, bytes, None] = None, content_type: Optional[str] = None, headers: Optional[dict] = None) -> Response:

        if not url.startswith("http"):
            url = f"https://service.aminoapps.com/api/v1{url}"

        if not headers:
            headers = self.session.headers.copy()

        if method.upper() == "GET":
            try:
                self.threads.append(self._responses.append(self.session.get(url=url, headers=headers)))
            except ReadTimeout:
                self.session.get(url=url, headers=headers).text
            
        if method.upper() == "DELETE":
            try:
                self.threads.append(self._responses.append(self.session.delete(url=url, headers=headers)))
            except ReadTimeout:
                self.session.delete(url=url, headers=headers).text

        if method.upper() == "POST":
            if not content_type:
                data = dumps(data)

            else:
                headers.update({"Content-Type": content_type})

            headers.update({"CONTENT-LENGTH": f"{len(data)}"})
            headers.update({"NDC-MSG-SIG": signature(data)})
            try:
                self.threads.append(self._responses.append(self.session.post(url=url, data=data, headers=headers)))
            except ReadTimeout:
                self.session.post(url=url, data=data, headers=headers).text
        
        response: Response = self._responses.pop(0)

        if self.debug:
            print(f'\n"Method": {method},\n"URL": {url},\n"Headers": {headers},\n"Response": {response.text}\n\n')

        if response.status_code  != 200:
            raise Exception(response.text)

        return loads(response.text)

        

