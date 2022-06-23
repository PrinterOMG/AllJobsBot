import string

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
DATABASE_URL = env.str("DATABASE_URL")

TRANSLATE_TABLE = str.maketrans(dict.fromkeys(string.punctuation))

PARSING_INTERVAL = 60  # In seconds

WEBLANCER_PAGES_COUNT = 4
