import logging
import os
from bot import RussianCasino
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = RussianCasino.create()
logger = logging.getLogger(__name__)

bot.load_extensions("cogs")
token = os.getenv("TOKEN")
bot.run(token)
