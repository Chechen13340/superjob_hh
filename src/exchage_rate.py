import requests

from superjob_hh.settings import API_KEY, ER_API_URL


def get_currency_rate(base='USD') -> float:
    """Получает курс доллара по API и вовзращает float"""

    response = requests.get(ER_API_URL, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    return rate

