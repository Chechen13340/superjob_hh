import json

import requests

from superjob_hh.settings import HH_API_URL, OPEARTION_PATH
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
        return data['items']

    def add_vacancies_file(self):
        vacancy = []
        for item in self.get_data():
            self.user_data = dict()
            self.user_data['job_title'] = item['name']
            self.user_data['location'] = item['area']['name']
            self.user_data['employer'] = item['employer']['name']
            self.user_data['url'] = item['alternate_url']
            self.user_data['requirement'] = item['snippet']['requirement']
            self.user_data['responsibilities'] = item['snippet']['responsibility']
            if item.get('salary') is None:
                self.user_data['salary_min'] = 0
                self.user_data['salary_max'] = 0
                self.user_data['currency'] = 'Информация отсутсвует'
            else:
                self.user_data['salary_min'] = item['salary']['from']
                self.user_data['salary_max'] = item['salary']['to']
                self.user_data['currency'] = item['salary']['currency']

            vacancy.append(self.user_data)

        return vacancy


class JSONSaver(HeadHunterParser):
    def __init__(self, vacansy_name: str, region: int, page_number: int, count_per_page: int):
        super().__init__(vacansy_name, region, page_number, count_per_page)

    def save_json(self):
        with open('../superjob_hh/vacancy.csv', 'w', newline='', encoding='utf8') as file:
            new_file = file.write(json.dumps(self.add_file(), indent=2, ensure_ascii=False))
            return new_file


class Vacancies:

    def __init__(self):
        self.job_title = None
        self.location = None
        self.employer = None
        self.url = None
        self.requirement = None
        self.responsibilities = None
        self.currency = None
        self.salary_max = None
        self.salary_min = None
        self.salary_average = None

        with open(OPEARTION_PATH, 'r', encoding='utf8') as file:
            self.data = json.load(file)

    def display_information(self):
        display_data = []
        for item in self.data:
            self.job_title = item['job_title']
            self.location = item['location']
            self.employer = item['employer']
            self.url = item['url']
            self.requirement = item['requirement']
            self.responsibilities = item['responsibilities']
            self.currency = item['currency']
            if item['salary_max'] is None:
                self.salary_min = item['salary_min']
                self.salary_max = 'Не указано'
                self.salary_average = self.salary_min
            elif item['salary_min'] is None:
                self.salary_max = item['salary_max']
                self.salary_min = 'Не указано'
                self.salary_average = self.salary_max
            else:
                self.salary_max = item['salary_max']
                self.salary_min = item['salary_min']
                self.salary_average = (int(self.salary_max) + int(self.salary_min)) // 2

            user_information = (f"\nДолжность: {self.job_title}\nЛокация: {self.location}\nРаботадатель: "
                                f"{self.employer}\nСайт вакансии: {self.url}\nТребования: {self.requirement}\n"
                                f"Обязанности: {self.responsibilities}\nЗаработная плата от: {self.salary_min}\n"
                                f"Заработная плата до: {self.salary_max}\n"
                                f"Средняя заработная плата: {self.salary_average}\nВалюта: {self.currency}\n")

            display_data.append(user_information)
        return display_data
