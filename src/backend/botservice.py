import requests
from telegram import *
from telegram.ext import *
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import os
from dataclasses import dataclass

class BotService:
    def __init__(self) -> None:
        load_dotenv()
        self.TOKEN = os.getenv('API_KEY')

class YoinkBotSender:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv('API_KEY')
        self.chat_ids = self.get_chat_ids()

    def send_message(self, message):
        for chat_id in self.chat_ids:
            url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            print(requests.get(url).json()) # this sends the message
    def get_chat_ids(self) -> list[str]:
        if os.path.exists('./data/chat_ids.txt'):
            with open('./data/chat_ids.txt', 'r') as f:
                chat_ids = f.read().splitlines()
        else:
            raise FileNotFoundError
        return chat_ids

class YoinkBotPollingService:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.application = ApplicationBuilder().token(os.getenv('API_KEY')).build()
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ahoi Matrose, Ich bin Yoink :)")
        self.save_chat_id(update.effective_chat.id)
        
    def save_chat_id(self, id):
        if not os.path.exists('./data/chat_ids.txt'):
            with open('./data/chat_ids.txt', 'w') as f:
                f.write(str(id) + '\n')
        else:
            with open('./data/chat_ids.txt', 'r') as f:
                chat_ids = f.readlines()
            chat_ids = [int(x.strip()) for x in chat_ids]
            if id not in chat_ids:
                with open('./data/chat_ids.txt', 'a') as f:
                    f.write(str(id) + '\n')
    def run(self):
        self.application.run_polling()