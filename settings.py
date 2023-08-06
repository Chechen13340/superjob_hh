from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent
OPEARTION_PATH = Path.joinpath(ROOT_PATH, 'vacancy.csv')

HH_API_URL = 'https://api.hh.ru/vacancies'

ER_API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv('API_KEY_Ex_Rate')
