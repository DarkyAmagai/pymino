import contextlib
import sys
from typing import Optional

from pymino.ext import console, context

__all__ = ("ChatConsole",)

HELP_MESSAGE = """
Chatroom Help:
    - Type any message to send it to the chat.
    - Type 'reply' to reply to a message.
    - Type 'sticker' to send a sticker.
    - Type 'leave' to leave the chat.
    - Type 'exit' to return to the main menu.
    - Type 'help' to see this message again.
    - Type 'clear' to clear the chat.
"""


class ChatConsole:
    def __init__(self, console: "console.Console") -> None:
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
        self.help_message = HELP_MESSAGE
        self.replies: dict[int, str] = {}

    def join_public_chat(self) -> None:
        """
        Handles joining of a public chat.
        """
        if not self.console.bot.community_id:
            self.console.on_error("You must select a community first.")
            return None
        self.console.print("Join Public Chat")
        self.console.print("""
    1. Join by Chat ID
    2. Join by Link
    3. Find Public Chats To Join
    4. Back
    """)
        back_option, choice = 4, 0
        while choice not in range(1, back_option + 1):
            with contextlib.suppress(ValueError):
                choice = int(self.console.input(">>> "))
        if choice == back_option:
            return
        self.console.print()

        try:
            if choice == 1:
                chat_id = None
                while not chat_id:
                    chat_id = self.console.input("Enter chat ID: ")
            elif choice == 2:
                chat_link = None
                while not chat_link:
                    chat_link = self.console.input("Enter chat link: ")
                chat_id = self.console.bot.community.fetch_object_id(chat_link)
            else:
                self.console.clear()
                self.console.print("Find Public Chats To Join")
                public_chats = self.console.bot.community.fetch_public_chats(
                    size=25
                )
                if not public_chats.chatId:
                    self.console.print("Public Chats Not Found")
                    self.console.sleep(2)
                    return
                for index, (chat_id, chat_title) in enumerate(
                    zip(public_chats.chatId, public_chats.title), 1
                ):
                    self.console.print(f"{index}. {chat_title} ({chat_id})")
                self.console.print(f"{back_option}. Back\n")
                back_option, choice = len(public_chats.chatId) + 1, 0
                while choice not in range(1, back_option + 1):
                    with contextlib.suppress(ValueError):
                        choice = int(self.console.input(">>> "))
                if choice == back_option:
                    return
                chat_id = public_chats.chatId[choice - 1]
            self.console.bot.community.join_chat(chat_id)
            self.console.print("Joined chat successfully.")
        except Exception as exc:
            self.console.print(f"Error: {exc}")
        finally:
            self.console.sleep(2)

    def my_chats(self) -> None:
        """
        Lists the user's chats and allows them to interact with selected chat.
        """
        if not self.console.bot.community_id:
            self.console.on_error("You must select a community first.")
            return
        chat_id, chat_title = self.select_chat()
        if chat_id and chat_title:
            self.interact_with_chat(chat_id, chat_title)

    def select_chat(self) -> tuple[Optional[str], Optional[str]]:
        """
        Prints the user's chats.
        """
        self.console.print("My Chats")
        chats = self.console.bot.community.fetch_chats()
        chat_titles: list[str] = []
        chat_ids: list[str] = []
        for index, (chatId, title) in enumerate(zip(chats.chatId, chats.title), 1):
            if title is None:
                chat_users = self.console.bot.community.fetch_chat_members(chatId)
                title = ", ".join(chat_users.members.nickname[:3]) + " [Private Chat]"
            else:
                title = f"{title} [Public Chat]"
            self.console.print(f"{index}. {title}({chatId})")
            chat_titles.append(title)
            chat_ids.append(chatId)
        self.console.print("\nType 'back' to go back to the menu.\n")
        # target selector
        chat_id, chat_title = None, None
        while not chat_id:
            choice_raw = self.console.input(">>> ")
            if choice_raw == "back":
                break
            try:
                choice = int(choice_raw)
            except ValueError:
                self.console.print("Invalid option. Please try again.")
                continue
            if choice not in range(1, len(chat_ids) + 1):
                self.console.print("Invalid option. Please try again.")
                continue
            chat_id, chat_title = chat_ids[choice - 1], chat_titles[choice - 1]
        return chat_id, chat_title

    def interact_with_chat(self, chat_id: str, chat_title: str):
        """
        Allows the user to interact with the selected chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :param chat_title: Title of the chat.
        :type chat_title: str
        :return: None
        """
        self.console.clear()
        self.console.print(f"Chat: {chat_title}")
        self.initiate_message_listener(chat_id)
        self.console.print(self.help_message)
        while self.handle_chat_interaction(chat_id, chat_title):
            self.console.sleep(2)
        self.console.print("\nReturning to Main Menu.\n")
        self.console.sleep(2)

    def initiate_message_listener(self, chat_id: str):
        counter = 0

        @self.console.bot._console_on_text_message()  # type: ignore
        def _(ctx: "context.Context"):
            nonlocal counter
            if ctx.chatId == chat_id:
                self.console.print()
                self.replies[counter] = ctx.message.messageId
                self.console.print(
                    f"[{counter}] {ctx.author.nickname}: {ctx.message.content}"
                )
                counter += 1
                sys.stdout.write(" " * self.console.indent_size + ">>> ")
                sys.stdout.flush()

    def handle_chat_interaction(
        self, chat_id: str, chat_title: Optional[str] = None
    ) -> bool:
        continue_interactions = True
        try:
            message = self.console.input(">>> ")
            if message in {"exit", "quit", ""}:
                self.handle_leave(None)
                continue_interactions = False
            elif message == "reply":
                self.handle_reply(chat_id)
            elif message == "sticker":
                self.handle_sticker(chat_id)
            elif message == "leave":
                self.handle_leave(chat_id)
            elif message == "help":
                self.console.print(self.help_message)
            elif message == "clear":
                self.console.clear()
                self.console.print(f"Chat: {chat_title}")
            else:
                self.console.bot.community.send_message(
                    chatId=chat_id, content=message
                )
                self.console.print(f"You: {message}")
        except EOFError:
            self.console.print("\n")
            sys.stdout.write(">>> ")
            sys.stdout.flush()
        return continue_interactions

    def handle_reply(self, chat_id: str) -> None:
        self.console.print("Enter the message ID of the message you want to reply to.")
        reply_index_raw = self.console.input(">>> ")
        if reply_index_raw in {"exit", "quit", ""}:
            return
        try:
            reply_index = int(reply_index_raw)
        except ValueError:
            self.console.print("Invalid message ID. Please try again.")
            return
        if reply_index not in self.replies:
            self.console.print("Invalid Reply Index. Please try again.")
            return
        self.console.print("Enter your reply.")
        reply = self.console.input(">>> ")
        if reply in {"exit", "quit", ""}:
            return
        self.console.bot.community.reply_message(
            chatId=chat_id, content=reply, messageId=self.replies[reply_index]
        )
        self.console.print(f"You: {reply}")

    def handle_sticker(self, chat_id: str) -> None:
        """
        Handles sending a sticker in the chat.

        :param chat_id: ID of the chat.
        :type chat_id: str
        :return: True if the interaction should continue, False otherwise.
        :rtype: bool
        """
        if not self.stickers:
            self.console.print(f"Empty pymino sticker")
            return
        back_option = len(self.stickers) + 1
        for key, value in self.stickers.items():
            self.console.print(f"[{key}] {list(value)[0]}")
        self.console.print(f"[{back_option}] Cancell sending")
        self.console.print("Enter the key of the sticker you want to send.")
        self.console.print("Example: >>> 1")
        while True:
            raw_choice = self.console.input(">>> ")
            try:
                choice = int(raw_choice)
            except ValueError:
                if raw_choice in {"exit", "quit", ""}:
                    return
                self.console.print("Invalid Option. Please try again.")
                continue
            if choice not in range(1, back_option + 1):
                self.console.print("Invalid Option. Please try again.")
                continue
            break
        _, sticker_id = self.stickers[choice]
        try:
            self.console.bot.community.send_sticker(chat_id, stickerId=sticker_id)
        except Exception:
            pass
        else:
            self.console.print(f"You: {sticker_id}")

    def handle_leave(self, chat_id: Optional[str]) -> None:
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
        self.console.bot._events.pop("_console_text_message", None)  # type: ignore
        self.console.print("Left chat successfully.")
        self.console.sleep(2)
