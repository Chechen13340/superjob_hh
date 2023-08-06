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
        return data['items']


class JSONSaver(HeadHunterParser):
    def __init__(self, vacansy_name: str, region: int, page_number: int, count_per_page: int):
        super().__init__(vacansy_name, region, page_number, count_per_page)

    def data_dict(self) -> dict:
        vacancy = []
        for item in self.get_data():
            user_data = dict()
            user_data['job_title'] = item['name']
            user_data['location'] = item['area']['name']
            user_data['employer'] = item['employer']['name']
            user_data['url'] = item['alternate_url']
            user_data['requirement'] = item['snippet']['requirement']
            user_data['responsibilities'] = item['snippet']['responsibility']
            if item.get('salary') is None:
                user_data['salary_min'] = 0
                user_data['salary_max'] = 0
                user_data['currency'] = 'Информация отсутсвует'
            else:
                user_data['salary_min'] = item['salary']['from']
                user_data['salary_max'] = item['salary']['to']
                user_data['currency'] = item['salary']['currency']

            vacancy.append(user_data)

        return vacancy

    def save_json(self):
        with open('../superjob_hh/vacancy.csv', 'w', newline='', encoding='utf8') as file:
            new_file = file.write(json.dumps(self.data_dict(), indent=2, ensure_ascii=False))
            return new_file
