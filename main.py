import logging
import os
from bot import CasinoBot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = CasinoBot.create()
logger = logging.getLogger(__name__)

bot.load_extensions("cogs")
token = os.getenv("TOKEN")
bot.run(token)
