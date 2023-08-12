from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent
OPEARTION_PATH_HH = Path.joinpath(ROOT_PATH, 'vacancy.csv')
OPEARTION_PATH_SJ = Path.joinpath(ROOT_PATH, 'vacancy_sj.csv')
SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
HH_API_URL = 'https://api.hh.ru/vacancies'

ER_API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv('API_KEY_Ex_Rate')
