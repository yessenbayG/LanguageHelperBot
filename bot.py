import telebot, sqlite3
from config_data import load_config


bot = telebot.Telebot(load_config().tg_bot)

