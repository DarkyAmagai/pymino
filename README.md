# pymino
# API wrapper for Amino apps
#

# Installation
# ------------
# pip install pymino

# Usage
# -------
```py
>>> from pymino import *
>>> from pymino.ext.context import Context
>>>
>>> client = Client()
>>>
>>> @client.on_ready()
... def ready():
...     print(f"{client.profile.username} has logged in!")

>>> @client.on_text_message()
... def message(ctx: Context):
...     print(f"{ctx.author.username}: {ctx.message.content}")
...     if ctx.message.content.startswith("hi"):
...         ctx.reply("Hello!")

>>> @client.on_member_join()
... def join(ctx: Context):
...     ctx.reply(f"Welcome to the chat, {ctx.author.username}!")
...
>>> @client.on_member_leave()
... def leave(ctx: Context):
...     ctx.reply(f"Goodbye!")
...
>>> @client.command("ping")
... def ping(ctx: Context):
...     ctx.reply("Pong!")
...
>>> @client.task(interval=10)
... def task():
...     print("This is a task! It will run every 10 seconds!")
...
>>> @client.on_error()
... def error(error: Exception):
...     print(f"An error has occurred: {error}")
...
>>> client.run("email", "password") or client.run("sid")
```
# Documentation
# -------------
# https://pymino.readthedocs.io/en/latest/
#
#


