import telebot, sqlite3
from config_data import load_config


bot = telebot.TeleBot(load_config().tg_bot.token)

#connect to database SQLite
conn = sqlite3.connect('language_helper.db', check_same_thread=False)
cursor = conn.cursor()

#Создание таблицы для хранения слов и фраз
cursor.execute('''CREATE TABLE IF NOT EXISTS phrases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE,
                    translation TEXT,
                    example TEXT)''')
conn.commit()

#Добавление слов и фраз в базу данных
phrases = [
    ("hello", "привет", "Hello! How are you?"),
    ("goodbye", "до свидания", "Goodbye! See you later."),
    ("thank you", "спасибо", "Thank you for your help."),
    ("please", "пожалуйста", "Please, can you pass the salt?")
]

cursor.executemany('INSERT OR IGNORE INTO phrases (word, translation, example) VALUES (?, ?, ?)', phrases)
conn.commit()


#Функция для получения случайной фразы из базы данных
def get_random_phrase():
    cursor.execute('SELECT word, translation, example FROM phrases ORDER BY RANDOM() LIMIT LIMIT 1')
    return cursor.fetchone()

