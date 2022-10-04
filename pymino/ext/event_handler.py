from time import sleep, time
from threading import Thread as threadIt
from .context import Context

class EventHandler:
    """
    `EventHandler` is a class that handles events.
    command_prefix = "!"

    `**Example**`
    ```python

    from pymino import Client
    from pymino.ext.context import Context

    bot = Client()

    @bot.on_ready()
    def on_ready():
        print("Bot is ready!")

    @bot.on_message()
    def on_message(ctx: Context):
        print(ctx.message.content)

    bot.run(email, password) or bot.run(sid)

    ```
    """

    def __init__(self):
        self._events = {}
        self._commands = {}
        self.command_prefix = "!"

    def _handle_event(self, event: str, data: dict):
        if event == "member_join":
            self._events["member_join"](Context(data))
        elif event == "member_leave":
            self._events["member_leave"](Context(data))
        elif event == "text_message":
            self._events["text_message"](Context(data))
            
    def on_ready(self):
        def decorator(func):
            self._events["ready"] = func
            return func
        return decorator

    def on_text_message(self):
        """
        `on_text_message` is a decorator that handles the `text_message` event.

        `**Example**`
        ```python
        from pymino import Client

        bot = Client()

        @bot.on_text_message()
        def on_text_message(ctx: Context):
            print(ctx.message.content)
        
        bot.run("email", "pass") or bot.run("sid")
        ```

        """
        def decorator(func):
            self._events["text_message"] = func
            return func
        return decorator

    def on_member_join(self):
        """
        `on_member_join` is a decorator that handles the `member_join` event.

        `**Example**`
        ```python
        from pymino import Client

        bot = Client()

        @bot.on_member_join()
        def on_member_join(ctx: Context):
            ctx.send(f"Welcome {ctx.author.username}!")

        bot.run("email", "pass") or bot.run("sid")
        ```
        """
        def decorator(func):
            self._events["member_join"] = func
            return func
        return decorator

    def on_member_leave(self):
        """
        `on_member_leave` is a decorator that handles the `member_leave` event.

        `**Example**`
        ```python
        from pymino import Client

        bot = Client()

        @bot.on_member_leave()
        def on_member_leave(ctx: Context):
            ctx.send(f"{ctx.author.username} left the chat!")

        bot.run("email", "pass") or bot.run("sid")
        ```
        """
        def decorator(func):
            self._events["member_leave"] = func
            return func
        return decorator

    def on_error(self):
        """
        `on_error` is a decorator that handles the `error` event.
        """
        def decorator(func):
            self._events["error"] = func
            return func
        return decorator

    def command(self, name: str):
        """
        @bot.command("ping")
        def do_stuff(ctx: Context, community: Community):
            ctx.reply("Pong!")
            community.send_link_snippet(
                chatId=community.fetch_chats().chatId[0],
                message="Hello, world!",
                image=open("temp.png", "rb")
            )
        ```
        """
        def decorator(func):
            self._commands[name] = func
            return func
        return decorator

    def emit(self, name: str, *args):
        """
        `emit` is a function that emits an event.

        `**Example**`
        ```python
        bot.emit("ready")
        ```

        """
        if name in self._events:
            self._events[name](*args)
    

    def start_task(self, func):
        """
        `start_task` is a function that starts a task.
        """
        threadIt(target=func).start()

    def task(self, interval: int = 10):
        """
        `task` is a decorator that handles tasks.

        `**Example**`
        ```python
        from pymino import Client

        bot = Client()

        @bot.task(interval=10)
        def task():
            for i in range(5):
                print("Task!")

        bot.run("email", "pass") or bot.run("sid")
        ```
        
        """
        def decorator(func):
            def wrapper():
                while True:
                    func()
                    sleep(interval)
            self.start_task(wrapper)
            return func
        return decorator
