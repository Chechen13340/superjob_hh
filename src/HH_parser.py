import json

import requests

from superjob_hh.settings import HH_API_URL
from superjob_hh.src.abstract_class import HH_SJ_API


class HeadHunterParser(HH_SJ_API):
    def __init__(self, vacansy_name: str, region: int, page_number: int, count_per_page: int):

        super().__init__(url=HH_API_URL, headers={"User-Agent": "HH-User-Agent"}, params={
            'text': vacansy_name,
            'area': region,
            'page': page_number,
            'per_page': count_per_page
        })

    def get_data(self) -> dict:
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data = response.json()
        with open('../vacansy.csv', 'w', newline='', encoding='utf8') as file:
            file.write(json.dumps(data['items'], indent=2, ensure_ascii=False))
        return data['items']

    def display_information(self) -> list:
        vacansy = []
        for item in self.get_data():
            vacancy_name = item['name']
            vacancy_area = item['area']['name']
            vacancy_employer = item['employer']['name']
            vacancy_url = item['alternate_url']
            vacancy_requirement = item['snippet']['requirement']
            vacancy_responsibility = item['snippet']['responsibility']
            if item.get('salary') is None:
                vacansy_salary_from = 'Не указано'
                vacansy_salary_to = 'Не указано'
                vacansy_currency = 'Информация отсутсвует'
            else:
                vacansy_salary_from = item['salary']['from']
                vacansy_salary_to = item['salary']['to']
                vacansy_currency = item['salary']['currency']
            data_vacancy = (f"Должность: {vacancy_name}\nГород: {vacancy_area}\nРаботодатель: "
                            f"{vacancy_employer}\nСайт вакансии: {vacancy_url}\nЗаработная плата от: "
                            f"{vacansy_salary_from} до {vacansy_salary_to} {vacansy_currency}\nОписание вакансии: "
                            f"{vacancy_requirement}\nОбязанности: {vacancy_responsibility}\n")

            vacansy.append(data_vacancy)

        return vacansy
