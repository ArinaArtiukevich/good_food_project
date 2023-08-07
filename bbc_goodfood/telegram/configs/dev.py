import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
# todo del загружаем в окружение
load_dotenv(env_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
FAST_API_RECOMMENDER_URL = os.getenv('FAST_API_RECOMMENDER_URL')
FAST_API_TELEGRAM_URL = os.getenv('FAST_API_TELEGRAM_URL')