import asyncio
from .dispatcher import AsyncMessageDispatcher


class QueueHandler:
    def __init__(self, message_queue: asyncio.Queue, dispatcher: AsyncMessageDispatcher) -> None:
        self.message_queue = message_queue
        self.dispatcher = dispatcher

    async def process_messages(self) -> None:
        while True:
            message = await self.message_queue.get()
            if message is None:
                break
            await self.dispatcher.handle(message)
            self.message_queue.task_done()