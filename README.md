# pymino
## A Python wrapper to communicate with Amino Apps API.
### Easily create a bot for Amino Apps using a modern easy to use synchronous library.
### If you have any questions or need help, feel free to join the [Discord server](https://discord.gg/JMJpzpsMNJ).
#
## Installation
### Recommended installation method is through pip.
```bash
pip install pymino
```
### Alternatively you can clone the repository and install it manually.
```bash
git clone https://github.com/forevercynical/pymino.git
```

```bash
cd pymino
```

```bash
python setup.py install
```


#
### Client Class Usage
```python
>>> from pymino import Client
...
>>> # Initialize the client
>>> client = Client() # You can set proxies and device_id here
...
... # You need to login to utilize most functions.
>>> client.login("email", "password") or client.login("sid")
>>> print(f"Logged in as {client.profile.username}")
...
... # We can either set community_id by link or by comId.
>>> client.fetch_community_id(community_link="https://aminoapps.com/c/OnePiece")
... # Or
>>> client.set_community_id(community_id=123)
...
... # To access community functions we utilize the community property.
>>> client.community.send_message(
...     chatId=000000-0000-0000-000000,
...     content="Hello world!"
... )
... # This will utilize the community id we set earlier.
... # We can also set the community id in the function call itself.
>>> client.community.send_message(
...     chatId=000000-0000-0000-000000,
...     content="Hello world!",
...     comId=123
...     )
```
#
### Bot Class Usage
```python
from pymino import Bot
from pymino.ext import *
...
... # Initialize the bot
>>> bot = Bot(
... command_prefix="!",
... community_id = 00000000,
... ) # You can set proxies and device_id here
...
... # The on_ready event is called when the bot has logged in.
>>> @bot.on_ready()
... def ready():
...     print(f"{bot.profile.username} has logged in!")
...
... # The on_text_message event is called when a message is received.
>>> @bot.on_text_message()
... def message(ctx: Context):
...     print(f"{ctx.author.username}: {ctx.message.content}")
...     if ctx.message.content.startswith("hi"):
...         ctx.reply("Hello!")
...
... # The on_member_join event is called when a member joins a chat.
>>> @bot.on_member_join()
... def join(ctx: Context):
...     ctx.reply(f"Welcome to the chat, {ctx.author.username}!")
...
... # The on_member_leave event is called when a member leaves a chat.
>>> @bot.on_member_leave()
... def leave(ctx: Context):
...     ctx.reply(f"Goodbye!")
...
... # This is how you create a command.
>>> @bot.command(
...     command_name = "ping", # Set the name of the command.
...     command_description = "This will reply with Pong!", # Set the description of the command.
...     command_aliases = ["p"], # Set the aliases of the command. This will allow !p to be used as !ping.
...     cooldown = 0 # Set the cooldown of the command. This will prevent the command from being used for <cooldown> seconds.
...     )
... def ping(ctx: Context): # The context is passed to the function.
...     ctx.reply("Pong!") # This will reply to the message with "Pong!"
...
>>> @bot.command("say")
... def say(ctx: Context, message: str): # message will be the content message after the command.
...     ctx.reply(message) # This will reply to the message with the message argument.
...
>>> @bot.task(interval=10) # This will run any task every 10 seconds.
... def task(): # This will not use community functions.
...     print("This is a task! It will run every 10 seconds!")
...
>>> @bot.task(interval=30)
... def task(community: Community):
...     [...] # Do something in the community
...     community.send_message(chatId, "Hello world!")
...     print("This is a community task! It will run every 30 seconds.")
...
>>> @bot.on_error()
... def error(error: Exception): # This will be called when an error occurs.
...     print(f"An error has occurred: {error}")
...
>>> bot.run("email", "password") or bot.run("sid") # You can login with email and password or sid.

```

# Documentation
### The documentation is available on the [website](https://pymino.info/index.html).
#