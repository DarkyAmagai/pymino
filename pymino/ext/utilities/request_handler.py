from .generate import *

class RequestHandler:
    """A class that handles all requests"""
    def __init__(self, bot, session: ClientSession, proxy: Optional[str] = None):
        self.bot        = bot
        self.session:   ClientSession = session
        self.proxy:     Optional[str] = proxy
        self.queue:     Queue = Queue()
        self.loop:      AbstractEventLoop = get_event_loop()

    def handler(self, **kwargs) -> dict:
        with suppress(ServerDisconnectedError, ClientConnectorError):
            if any([kwargs.get("wait"), kwargs.get("wait") is None]):
                response = self.loop.run_until_complete(self.process(**kwargs))
                return response if response else {}

            async def create_task():
                await self.queue.put(await self.process(**kwargs))
            return [self.queue.get_nowait(self.loop.run_until_complete(self.loop.create_task(create_task())))]

    async def process(self, method: str, url: str, data: Union[dict, bytes, None] = None, content_type: Optional[str] = None, **kwargs):
        url = f"https://service.aminoapps.com/api/v1{url}"

        headers = {**self.session.headers, "NDCDEVICEID": device_id()}
        request_methods = {"GET": self.session.get, "POST": self.session.post, "DELETE": self.session.delete}
        
        if any([data, content_type]):
            data = dumps(data).decode() if not isinstance(data, bytes) else data
            headers.update({
                "CONTENT-LENGTH": f"{len(data)}",
                "NDC-MSG-SIG": signature(data),
                "CONTENT-TYPE": content_type if content_type is not None else "application/json; charset=utf-8"
                })

        async with request_methods[method](url, data=data, headers=headers, proxy=self.proxy) as response:
            response: ClientResponse = response

            if response.status != 200:
                with suppress(Exception):
                    response_json: dict = loads(await response.text())
                    # TODO: Handle exceptions.
                    if response_json.get("api:statuscode") == 105: return self.bot.run(self.email, self.password)

                raise Exception(await response.text())

            return loads(await response.text())