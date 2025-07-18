from collections.abc import Callable
from typing import Any

__all__ = ("MessageDispatcher",)

Handler = Callable[[dict[str, Any]], None]


class MessageDispatcher:
    """Simple message dispatcher that allows you to register handlers for specific message types.

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

    def __init__(self) -> None:
        self.dispatch_table: dict[int, set[Handler]] = {}

    def register(self, message_type: int, handler: Handler) -> None:
        self.dispatch_table.setdefault(message_type, set()).add(handler)

    def handle(self, message: dict[str, Any]) -> None:
        message_type = message.get("t", 0)
        if message_type not in self.dispatch_table:
            return None
        for handler in self.dispatch_table[message_type]:
            handler(message)
