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


def get_random_phrase():
    cursor.execute('SELECT word, translation, example FROM phrases ORDER BY RANDOM() LIMIT 1')
    return cursor.fetchone()


def add_phrase(word, translation, example):
    cursor.execute('INSERT INTO phrases (word, translation, example) VALUES (?, ?, ?)', (word, translation, example))
    conn.commit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я LanguageHelperBot."
                     "Отправь команду /phrase, чтобы получить случайное слово или фразу для изучения."
                     "Отправь команду /add слово, перевод, пример, чтобы добавить новую фразу.")


@bot.message_handler(commands=['phrase'])
def send_phrase(message):
    word, translation, example = get_random_phrase()

    phrase_message = (f"Слово: {word}\n"
                      f"Перевод: {translation}\n"
                      f"Пример: {example}")
    bot.send_message(message.chat.id, phrase_message)


@bot.message_handler(commands=['add'])
def add_new_phrase(message):
    try:
        # Удаляем команду /add и разбиваем оставшийся текст на части
        parts = message.text[len('/add'):].split(',')
        if len(parts) != 3:
            raise ValueError("Неверное количество аргументов")

        word, translation, example = map(str.strip, parts)

        add_phrase(word, translation, example)
        bot.send_message(message.chat.id, f"Фраза '{word}' успешно добавлена!")
    except ValueError:
        bot.send_message(message, "Пожалуйста, используйте формат: /add слово, перевод, пример")


bot.infinity_polling()