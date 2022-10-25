# pymino
## A Python wrapper for AminoApps API
### Library to create bots on Amino.
### Easily write your own bot with commands, tasks, and more.
#
## Installation
```bash
pip install pymino
```
#
### Usage
```python
>>> from pymino import *
>>> from pymino.ext import *
>>>
>>> bot = Bot(
...     command_prefix="!",
...     community_id = 00000000,
... )   # You can set proxies and device_id here
...
>>>
>>> @bot.on_ready()
... def ready():
...     print(f"{bot.profile.username} has logged in!")
...
>>> @bot.on_text_message()
... def message(ctx: Context):
...     print(f"{ctx.author.username}: {ctx.message.content}")
...     if ctx.message.content.startswith("hi"):
...         ctx.reply("Hello!")
...
>>> @bot.on_member_join()
... def join(ctx: Context):
...     ctx.reply(f"Welcome to the chat, {ctx.author.username}!")
...
>>> @bot.on_member_leave()
... def leave(ctx: Context):
...     ctx.reply(f"Goodbye!")
...
>>> @bot.command("ping")
... def ping(ctx: Context):
...     ctx.reply("Pong!")
...
>>> @bot.command("say")
... def say(ctx: Context, message: str):
...     ctx.reply(message)
...
>>> @bot.task(interval=10)
... def task():
...     print("This is a task! It will run every 10 seconds!")
...
>>> @bot.task(interval=30)
... def task(community: Community):
...     [...] # Do something in the community
...     community.send_message(chatId, "Hello world!")
...     print("This is a community task! It will run every 30 seconds.")
...
>>> @bot.on_error()
... def error(error: Exception):
...     print(f"An error has occurred: {error}")
...
>>> bot.run("email", "password") or bot.run("sid")
```
# Documentation
### Feel free to read the documentation [here](https://pymino.info/index.html).
#


