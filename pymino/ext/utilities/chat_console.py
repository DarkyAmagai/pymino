import sys


class ChatConsole:
    def __init__(self, console):
        """
        The ChatConsole class handles chat related operations in the application.

        :param console: An instance of the Console class for inter-component communication.
        :type console: Console
        """
        self.console = console
        self.stickers = {
            1: {"Laughing emoji": "e/f09f9882"},
            2: {"Nervous emoji": "e/f09f9885"},
            3: {"Nerd emoji": "e/f09fa493"},
            4: {"Sleep emoji": "e/f09f98b4"},
            5: {"Annoyed emoji": "e/f09f9892"},
            6: {"Sob emoji": "e/f09f98ad"},
            7: {"Angel emoji": "e/f09f9887"},
            8: {"Cowboy emoji": "e/f09fa4a0"},
            9: {"Clown emoji": "e/f09fa4a1"},
            10: {"Smirk emoji": "e/f09f988f"},

        }
        self.help_message = """
Chatroom Help:
    - Type any message to send it to the chat.
    - Type 'reply' to reply to a message.
    - Type 'sticker' to send a sticker.
    - Type 'leave' to leave the chat.
    - Type 'exit' to return to the main menu.
    - Type 'help' to see this message again.
    - Type 'clear' to clear the chat.
"""

    def join_public_chat(self):
        """
        Handles joining of a public chat.
        """
        if not self.console.bot.community_id:
            return self.console.on_error("You must select a community first.")

        self.console.print("Join Public Chat")
        self.console.print("""
    1. Join by Chat ID
    2. Join by Link
    3. Find Public Chats To Join
    4. Back
    """)
        choice = self.console.input(">>> ")
        self.console.print()

        try:
            if choice == "1":
                chat_id = self.console.input("Enter chat ID: ")
            elif choice == "2":
                chat_link = self.console.input("Enter chat link: ")
                chat_id = self.console.bot.community.fetch_object_id(chat_link)
            elif choice == "3":
                self.console.clear()
                self.console.print("Find Public Chats To Join")

                public_chats = self.console.bot.community.fetch_public_chats(size=25)
                for index, (chat_id, chat_title) in enumerate(zip(public_chats.chatId, public_chats.title)):
                    self.console.print(f"{index+1}. {chat_title}({chat_id})")

                self.console.print()
                choice = self.console.input(">>> ")
                self.console.print()

                try:
                    choice = int(choice)
                    if not (1 <= choice <= len(public_chats.chatId)):
                        raise ValueError
                    chat_id = public_chats.chatId[choice-1]
                except ValueError:
                    self.console.print("Invalid option. Please try again.")
                    return self.join_public_chat()

            elif choice == "4":
                return self.console.menu.display()

            else:
                self.console.print("Invalid option. Please try again.")
                return self.join_public_chat()

            self.console.bot.community.join_chat(chatId=chat_id)
            self.console.print("Joined chat successfully.")
            self.console.sleep(2)

        except Exception as e:
            self.console.print(f"Error: {e}")
            self.console.sleep(2)

        return self.console.menu.display()

    def my_chats(self):
        """
        Lists the user's chats and allows them to interact with selected chat.
        """
        if not self.console.bot.community_id:
            return self.console.on_error("You must select a community first.")
        self.print_chats()
        chat_id, chat_title = self.select_chat()
        if chat_id and chat_title:
            self.interact_with_chat(chat_id, chat_title)
        else:
            return self.console.menu.display()

    def print_chats(self):
        """
        Prints the user's chats.
        """
        self.console.print("My Chats")
        chats = self.console.bot.community.fetch_chats()
        for index, (chat_id, chat_title) in enumerate(zip(chats.chatId, chats.title)):
            if chat_title is None:
                chat_users = self.console.bot.community.fetch_chat_members(chat_id).members.nickname[:3]
                chat_title = ", ".join(chat_users) + "[Private Chat]"
            else:
                chat_title = f"{chat_title}[Public Chat]"
            self.console.print(f"{index+1}. {chat_title}({chat_id})")
        self.console.print("\nType 'back' to go back to the menu.\n")

    def select_chat(self):
        """
        Allows the user to select a chat.

        :return: Tuple containing chat ID and chat title, or (None, None) if back was selected.
        :rtype: Tuple[str, str]
        """
        choice = self.console.input(">>> ")
        self.console.print()
        if choice == "back":
            return None, None
        try:
            choice = int(choice)
            chats = self.console.bot.community.fetch_chats()
            if not (1 <= choice <= len(chats.chatId)):
                raise ValueError
            chat_id, chat_title = chats.chatId[choice-1], chats.title[choice-1]
            return chat_id, chat_title
        except ValueError:
            self.console.print("Invalid option. Please try again.")
            return self.select_chat()

    def interact_with_chat(self, chat_id: str, chat_title: str):
        """
        Allows the user to interact with the selected chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :param chat_title: Title of the chat.
        :type chat_title: str
        :return: None
        """
        self.replies = {}
        self.console.clear()
        self.console.print(f"Chat: {chat_title}")

        self.initiate_message_listener(chat_id)
        self.console.print(self.help_message)

        while self.handle_chat_interaction(chat_id, chat_title):
            self.console.sleep(2)

        self.console.print("\nReturning to Main Menu.\n")
        self.console.sleep(2)
        return self.console.menu.display()

    def initiate_message_listener(self, chat_id: str):
        """
        Initiates a message listener for the specified chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :return: None
        """
        counter = 0

        @self.console.bot._console_on_text_message()
        def on_message(ctx):
            nonlocal counter
            if ctx.chatId == chat_id:
                self.console.print()
                self.replies[counter] = ctx.message.messageId
                self.console.print(f"[{counter}] {ctx.author.nickname}: {ctx.message.content}")
                counter += 1
                sys.stdout.write(" "*self.console.indent_size + ">>> ")
                sys.stdout.flush()

    def handle_chat_interaction(self, chat_id: str, chat_title: str = None) -> bool:
        """
        Handles user input for interacting with the chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :return: True if the interaction should continue, False otherwise.
        :rtype: bool
        """
        try:
            message = self.console.input(">>> ")
            if message in {"exit", "quit", ""}:
                self.handle_leave(None)
                return False
            elif message == "reply":
                return self.handle_reply(chat_id)
            elif message == "sticker":
                return self.handle_sticker(chat_id)
            elif message == "leave":
                return self.handle_leave(chat_id)
            elif message == "help":
                self.console.print(self.help_message)
                return True
            elif message == "clear":
                self.console.clear()
                self.console.print(f"Chat: {chat_title}")
                return True
            else:
                self.console.bot.community.send_message(chatId=chat_id, content=message)
                self.console.print(f"You: {message}")
                return True
        except (EOFError):
            self.console.print("\n")
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            return True

    def handle_reply(self, chat_id: str) -> bool:
        """
        Handles replying to a message in the chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :return: True if the interaction should continue, False otherwise.
        :rtype: bool
        """
        self.console.print("Enter the message ID of the message you want to reply to.")
        message_id = self.console.input(">>> ")
        if message_id in {"exit", "quit", ""}:
            return True
        try:
            message_id = int(message_id)
        except ValueError:
            self.console.print("Invalid message ID. Please try again.")
            return True
        if message_id not in self.replies:
            self.console.print("Invalid message ID. Please try again.")
            return True
        self.console.print("Enter your reply.")
        reply = self.console.input(">>> ")
        if reply in {"exit", "quit", ""}:
            return True
        self.console.bot.community.reply_message(chatId=chat_id, content=reply, messageId=self.replies[message_id])
        self.console.print(f"You: {reply}")
        return True

    def handle_sticker(self, chat_id: str) -> bool:
        """
        Handles sending a sticker in the chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :return: True if the interaction should continue, False otherwise.
        :rtype: bool
        """
        
        for key, value in self.stickers.items():
            self.console.print(f"[{key}] {list(value.keys())[0]}")

        self.console.print("Enter the key of the sticker you want to send.")
        self.console.print("Example: >>> 1")


        sticker_id = self.console.input(">>> ")
        if sticker_id in {"exit", "quit", ""}:
            return True
        
        try:
            self.console.bot.community.send_sticker(chatId=chat_id, stickerId=self.stickers[int(sticker_id)][list(self.stickers[int(sticker_id)].keys())[0]])
            self.console.print(f"You: {sticker_id}")
            return True
        except Exception:
            self.console.print("Invalid sticker ID. Please try again.")
            return True
            

    def handle_leave(self, chat_id: str) -> bool:
        """
        Handles leaving the chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :return: False, as the user is leaving the chat.
        :rtype: bool
        """
        if chat_id:
            self.console.bot.community.leave_chat(chat_id)
            
        self.replies.clear()
        del self.console.bot._events["_console_text_message"]
        self.console.print("Left chat successfully.")
        self.console.sleep(2)
        return False
