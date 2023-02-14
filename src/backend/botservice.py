import requests
from telegram import *
from telegram.ext import *
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import __version__ as TG_VER
from dotenv import load_dotenv
import os
from message import Message
from dataclasses import dataclass
from controller import Controller


# class BotService:
#     def __init__(self) -> None:
#         load_dotenv()
#         self.TOKEN = os.getenv("API_KEY")


# class YoinkBotSender:
#     def __init__(self):
#         load_dotenv()
#         self.TOKEN = os.getenv("API_KEY")
#         self.chat_ids = self.get_chat_ids()

#     def send_message(self, message):
#         for chat_id in self.chat_ids:
#             url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#             print(requests.get(url).json())  # this sends the message

#     def get_chat_ids(self) -> list[str]:
#         if os.path.exists("./data/chat_ids.txt"):
#             with open("./data/chat_ids.txt", "r") as f:
#                 chat_ids = f.read().splitlines()
#         else:
#             raise FileNotFoundError
#         return chat_ids


# class YoinkBotPollingService:
#     def __init__(self):
#         logging.basicConfig(
#             format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#             level=logging.INFO,
#         )

#     async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         await context.bot.send_message(
#             chat_id=update.effective_chat.id, text="Ahoi Matrose, Ich bin Yoink :)"
#         )
#         self.save_chat_id(update.effective_chat.id)

#     def save_chat_id(self, id) -> None:
#         if not os.path.exists("./data/chat_ids.txt"):
#             with open("./data/chat_ids.txt", "w") as f:
#                 f.write(str(id) + "\n")
#         else:
#             with open("./data/chat_ids.txt", "r") as f:
#                 chat_ids = f.readlines()
#             chat_ids = [int(x.strip()) for x in chat_ids]
#             if id not in chat_ids:
#                 with open("./data/chat_ids.txt", "a") as f:
#                     f.write(str(id) + "\n")

#     def run(self):
#         self.application.run_polling()


class YoinkBot:
    def __init__(self) -> None:
        load_dotenv()
        self.TOKEN = os.getenv("API_KEY")
        self.application = Application.builder().token(self.TOKEN).build()

        # on different commands - answer in Telegram
        self.application.add_handler(CommandHandler(["start", "help"], self.start))
        self.application.add_handler(CommandHandler("unset", self.stop))

        try:

            from telegram import __version_info__

        except ImportError:
            __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

        if __version_info__ < (20, 0, 0, "alpha", 1):

            raise RuntimeError(
                f"This example is not compatible with your current PTB version {TG_VER}. To view the "
                f"{TG_VER} version of this example, "
                f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
            )

        # Enable logging
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        """Sends explanation on how to use the bot."""

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ahoi Matrose, Ich bin Yoink :)"
        )
        await update.message.reply_text("Use /list to see your items (aber noch nicht jetzt das funktioniert nämlich noch nicht)")
        await update.message.reply_text("Use /add <item-name> to add an item (aber noch nicht jetzt das funktioniert nämlich noch nicht)")
        await update.message.reply_text("Use /remove <item-name> to remove an item (aber noch nicht jetzt das funktioniert nämlich noch nicht)")
        await update.message.reply_text("Use /stop to stop my service (aber noch nicht jetzt das funktioniert nämlich noch nicht)")
        self.save_chat_id(update.effective_chat.id)

    def save_chat_id(self, id) -> None:
        if not os.path.exists("./data/chat_ids.txt"):
            with open("./data/chat_ids.txt", "w") as f:
                f.write(str(id) + "\n")
        else:
            with open("./data/chat_ids.txt", "r") as f:
                chat_ids = f.readlines()
            chat_ids = [int(x.strip()) for x in chat_ids]
            if id not in chat_ids:
                with open("./data/chat_ids.txt", "a") as f:
                    f.write(str(id) + "\n")

    def get_chat_ids(self) -> list[str]:
        if os.path.exists("./data/chat_ids.txt"):
            with open("./data/chat_ids.txt", "r") as f:
                chat_ids = f.read().splitlines()
        else:
            raise FileNotFoundError
        return chat_ids

    async def alarm(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the price-alarm message."""
        contr = Controller()
        contr.run()
        for chat_id in self.get_chat_ids():
            for msg in contr.pass_messages(chat_id):
                await context.bot.send_message(
                    chat_id, text=msg.msg)
            contr.after_sent(chat_id)


    def remove_job_if_exists(
        self, name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Remove job with given name. Returns whether job was removed."""

        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False

        for job in current_jobs:
            job.schedule_removal()

        return True

    def set_timer(self) -> None:
        """Add a job to the queue."""

        # try:
            # args[0] should contain the time for the timer in seconds
        # interval = 60
        interval = 60*60*3


        self.application.job_queue.run_repeating(
            self.alarm, interval, first=5)


            # job_removed = self.remove_job_if_exists(str(chat_id), context)
        #     text = "Timer successfully set!"
        #     if job_removed:
        #         text += " Old one was removed."
        #     await update.effective_message.reply_text(text)
        # except (IndexError, ValueError):
        #     await update.effective_message.reply_text("Usage: /set <seconds>")

    # async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #     """Remove the job if the user changed their mind."""
    #     chat_id = update.message.chat_id
    #     job_removed = self.remove_job_if_exists(str(chat_id), context)
    #     text = (
    #         "Timer successfully cancelled!"
    #         if job_removed
    #         else "You have no active timer."
    #     )
    #     await update.message.reply_text(text)

    def run(self) -> None:
        """Run bot."""
        # Run the bot until the user presses Ctrl-C
        self.set_timer()
        # self.application.start()
        self.application.run_polling()


bot = YoinkBot()
bot.run()
