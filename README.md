<div align="center">
  <h1 style="color: #0d47a1; font-size: 3em;">pymino</h1>
  
  <p>
    <a href="https://discord.gg/JMJpzpsMNJ"><img src="https://img.shields.io/discord/926853226152755280?color=blueviolet&label=discord%20server" alt="Discord"></a>
    <a href="https://libraries.io/github/forevercynical/pymino"><img src="https://img.shields.io/librariesio/github/forevercynical/pymino?color=blueviolet" alt="Libraries.io dependency status for GitHub repo"></a>
    <a href="https://github.com/forevercynical/pymino/commits/main"><img src="https://img.shields.io/github/last-commit/forevercynical/pymino?label=last%20updated&color=blueviolet" alt="GitHub last commit"></a>
    <a href="https://pypi.org/project/pymino/"><img src="https://img.shields.io/pypi/dw/pymino?color=blueviolet" alt="PyPI - Downloads"></a>
  </p>

  <p style="font-size: 1.2em; color: #424242;">A Python wrapper to communicate with the Amino Apps API.</p>
  <p style="font-size: 1.2em; color: #424242;">Easily create a bot for Amino Apps using a modern, easy-to-use library.</p>

  <div style="border: 3px solid red; padding: 10px; margin: 15px 0;">
    <h3 style="color: red;"><strong>WARNING</strong></h3>
    <p><strong>Pymino is a fully reverse-engineered client. By using this client, you may be violating the Amino Apps' Terms of Service. This could lead to your account being suspended or permanently banned. Please use Pymino responsibly and at your own risk.</strong></p>
    <p><strong>Understand that the developers and maintainers of Pymino are not responsible for any actions taken against your account as a result of using this client. Proceed with caution.</strong></p>
  </div>

  <p style="font-size: 1.2em; color: #424242;">If you have any questions or need help, feel free to join the Discord server.</p>
  
  <a href="https://discord.gg/JMJpzpsMNJ">
    <img src="https://cdn.discordapp.com/attachments/965797874791223317/1081754594977267833/discord-button.png" alt="Join Our Discord Server" width="150" height="50">
  </a>
  
  <h2 style="color: #0d47a1; font-size: 2em;">Installation</h2>
  
  <p style="font-size: 1.2em; color: #424242;">Recommended installation method is through pip:</p>
  
  <pre style="background-color: #f5f5f5; padding: 10px;"><code style="color: #f44336;">pip install pymino</code></pre>
  
  <p style="font-size: 1.2em; color: #424242;">Alternatively, you can clone the repository and install it manually:</p>
  
  <pre style="background-color: #f5f5f5; padding: 10px;"><code style="color: #f44336;">git clone https://github.com/forevercynical/pymino.git
  cd pymino
  python setup.py install</code></pre>
  
  <p style="font-size: 1.2em; color: #424242;">For more detailed documentation and usage examples, check out the project's <a href="https://pymino.info/index.html">official documentation</a>.</p>
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
...     console_enabled=True,
...     device_id=None,
...     intents=True,
...     online_status=True,
...     proxy="http://127.0.0.1:8080" # Must be a string.
... ) 

>>> # The on_ready event is called when the bot has logged in.
>>> @bot.on_ready()
... def ready():
...     print(f"{bot.profile.username} has logged in!")

>>> # The on_text_message event is called when a message is received.
>>> @bot.on_text_message()
... def message(ctx: Context, member: Member, message: str):
...     print(f"{member.username}: {message}")
...     if message.startswith("hi"):
...         ctx.reply("Hello!")

>>> # The on_member_join event is called when a member joins a chat.
>>> @bot.on_member_join()
... def join(ctx: Context, member: Member):
...     ctx.reply(f"Welcome to the chat, {member.username}!")

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
