
<div align="center">
  <h1>pymino</h1>
  
  [![Discord](https://img.shields.io/discord/926853226152755280?color=blueviolet&label=discord%20server)](https://discord.gg/JMJpzpsMNJ)
  [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/forevercynical/pymino?color=blueviolet)](https://libraries.io/github/forevercynical/pymino)
  [![GitHub last commit](https://img.shields.io/github/last-commit/forevercynical/pymino?label=last%20updated&color=blueviolet)](https://github.com/forevercynical/pymino/commits/main)
  [![PyPI - Downloads](https://img.shields.io/pypi/dw/pymino?color=blueviolet)](https://pypi.org/project/pymino/)
  
  <p>A Python wrapper to communicate with the Amino Apps API.</p>
  <p>Easily create a bot for Amino Apps using a modern, easy-to-use, synchronous library.</p>
  
  <p>If you have any questions or need help, feel free to join the Discord server.</p>
  
  <a href="https://discord.gg/JMJpzpsMNJ">
    <img src="https://cdn.discordapp.com/attachments/965797874791223317/1081754594977267833/discord-button.png" alt="Join Our Discord Server" width="150" height="50">
  </a>
  
  <h2>Installation</h2>
  
  <p>Recommended installation method is through pip:</p>
  
  <pre><code>pip install pymino</code></pre>
  
  <p>Alternatively, you can clone the repository and install it manually:</p>
  
  <pre><code>git clone https://github.com/forevercynical/pymino.git
  cd pymino
  python setup.py install</code></pre>
  
  <p>For more detailed documentation and usage examples, check out the project's <a href="https://pymino.info/index.html">official documentation</a>.</p>
</div>

<div>
  <h2 align="center">Client Class Usage</h2>

  <pre><code class="language-python">
>>> from pymino import Client

>>> # Initialize the client
>>> client = Client() # You can set proxies and device_id here

>>> # You need to login to utilize most functions.
>>> client.login("email", "password") or client.login("sid")
>>> print(f"Logged in as {client.profile.username}")

>>> # We can either set community_id by link or by comId.
>>> client.fetch_community_id(community_link="https://aminoapps.com/c/OnePiece")
>>> # Or
>>> client.set_community_id(community_id=123)

>>> # To access community functions we utilize the community property.
>>> client.community.send_message(
...     chatId=000000-0000-0000-000000,
...     content="Hello world!"
... )
>>> # This will utilize the community id we set earlier.
>>> # We can also set the community id in the function call itself.
>>> client.community.send_message(
...     chatId=000000-0000-0000-000000,
...     content="Hello world!",
...     comId=123
... )
  </code></pre>
</div>



<div>
  <h2 align="center">Bot Class Usage</h2>

  <pre><code class="language-python">
>>> from pymino import Bot
>>> from pymino.ext import *

>>> # Initialize the bot
>>> bot = Bot(
...     command_prefix="!",
...     community_id=00000000,
... ) # You can set proxies and device_id here

>>> # The on_ready event is called when the bot has logged in.
>>> @bot.on_ready()
... def ready():
...     print(f"{bot.profile.username} has logged in!")

>>> # The on_text_message event is called when a message is received.
>>> @bot.on_text_message()
... def message(ctx: Context):
...     print(f"{ctx.author.username}: {ctx.message.content}")
...     if ctx.message.content.startswith("hi"):
...         ctx.reply("Hello!")

>>> # The on_member_join event is called when a member joins a chat.
>>> @bot.on_member_join()
... def join(ctx: Context):
...     ctx.reply(f"Welcome to the chat, {ctx.author.username}!")

>>> # The on_member_leave event is called when a member leaves a chat.
>>> @bot.on_member_leave()
... def leave(ctx: Context):
...     ctx.reply(f"Goodbye!")

>>> # This is how you create a command.
>>> @bot.command(
...     name="ping", # Set the name of the command.
...     description="This will reply with Pong!", # Set the description of the command.
...     aliases=["p"], # Set the aliases of the command. This will allow !p to be used as !ping.
...     cooldown=0 # Set the cooldown of the command. This will prevent the command from being used for <cooldown> seconds.
... )
... def ping(ctx: Context): # The context is passed to the function.
...     ctx.reply("Pong!") # This will reply to the message with "Pong!"

>>> @bot.command("say")
... def say(ctx: Context, message: str): # message will be the content message after the command.
...     ctx.reply(message) # This will reply to the message with the message argument.

>>> @bot.task(interval=10) # This will run any task every 10 seconds.
... def task(): # This will not use community functions.
...     print("This is a task! It will run every 10 seconds!")

>>> @bot.task(interval=30)
... def task(community: Community):
...     [...] # Do something in the community
...     community.send_message(chatId, "Hello world!")
...     print("This is a community task! It will run every 30 seconds.")

>>> @bot.on_error()
... def error(error: Exception): # This will be called when an error occurs.
...     print(f"An error has occurred: {error}")

>>> bot.run("email", "password") or bot.run("sid") # You can login with email and password or sid.
  </code></pre>
</div>
