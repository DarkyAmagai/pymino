from typing import Callable

class MessageDispatcher:
    """
    `MessageDispatcher` - Simple message dispatcher that allows you to register handlers for specific message types.
 
    `**Example**`

    ```py

    dispatcher = MessageDispatcher()

    message_type = 1000
    message = {"t": message_type, "d": {"foo": "bar"}}
    handler = lambda message: print(message)

    dispatcher.register(message_type, handler)
    dispatcher.handle(message)
    ```

    """
    def __init__(self):
        self.dispatch_table = {}

    def register(self, message_type: int, handler: Callable):
        self.dispatch_table[message_type] = handler

    def handle(self, message: dict):
        message_type = message.get("t")
        if message_type not in self.dispatch_table:
            return None
        self.dispatch_table[message_type](message)


class AsyncMessageDispatcher:
    """
    `AsyncMessageDispatcher` - Simple async message dispatcher that allows you to register handlers for specific message types.
 
    `**Example**`

    ```py

    dispatcher = AsyncMessageDispatcher()

    message_type = 1000
    message = {"t": message_type, "d": {"foo": "bar"}}
    handler = lambda message: print(message)

    dispatcher.register(message_type, handler)
    await dispatcher.handle(message)
    ```

    """
    def __init__(self):
        self.dispatch_table = {}

    def register(self, message_type: int, handler: Callable):
        self.dispatch_table[message_type] = handler

    async def handle(self, message: dict):
        message_type = message.get("t")
        if message_type not in self.dispatch_table:
            return
        await self.dispatch_table[message_type](message)