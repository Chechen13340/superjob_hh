import json

import requests

from superjob_hh.settings import HH_API_URL
from superjob_hh.src.abstract_class import HH_SJ_API


class HeadHunterParser(HH_SJ_API):
    def __init__(self, vacancy_name: str, region: int, page_number: int, count_per_page: int):
        self.__vacancy_name = vacancy_name
        self.__region = region
        self.__page_number = page_number
        self.__count_per_page = count_per_page
        super().__init__(url=HH_API_URL, headers={"User-Agent": "HH-User-Agent"}, params={
            'text': vacancy_name,
            'area': region,
            'page': page_number,
            'per_page': count_per_page
        })

    @property
    def vacancy_name(self):
        return self.__vacancy_name

    @property
    def region(self):
        return self.__region

    @property
    def page_number(self):
        return self.__page_number

    @property
    def count_per_page(self):
        return self.__count_per_page

    def get_data(self) -> dict:
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data = response.json()
        return data['items']

    def del_data(self, key_word: str):
        """"
        Метод для удаления определенных данных
        из файла .txt, которые не нужны пользователю.
        """
        self.key_word = key_word
        with open("sort_data.txt") as file, open("del_data.txt", 'w') as new_file:
            for line in file:
                if key_word not in line:
                    new_file.write(line)
            return new_file


class Vacancies(HeadHunterParser):
    def __init__(self, vacancy_name: str, region: int, page_number: int, count_per_page: int, request_salary: str):
        self.request_salary = request_salary
        super().__init__(vacancy_name, region, page_number, count_per_page)

    def add_vacancies_file(self):
        """"
        Метод для добавления информауии о вакансиях в список
        словарей для последующей записи json файла.
        """
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
                self.user_data['salary_average'] = (self.user_data['salary_min'] + self.user_data['salary_max']) / 2
                self.user_data['currency'] = 'Информация отсутсвует'
            elif item['salary']['from'] is None:
                self.user_data['salary_min'] = 0
                self.user_data['salary_max'] = item['salary']['to']
                self.user_data['salary_average'] = self.user_data['salary_max']
                self.user_data['currency'] = item['salary']['currency']
            elif item['salary']['to'] is None:
                self.user_data['salary_min'] = item['salary']['from']
                self.user_data['salary_max'] = 0
                self.user_data['salary_average'] = self.user_data['salary_min']
                self.user_data['currency'] = item['salary']['currency']
            else:
                self.user_data['salary_min'] = item['salary']['from']
                self.user_data['salary_max'] = item['salary']['to']
                self.user_data['salary_average'] = (int(self.user_data['salary_min']) + int(
                    self.user_data['salary_max'])) // 2
                self.user_data['currency'] = item['salary']['currency']

            vacancy.append(self.user_data)

        return vacancy

    # @staticmethod
    def validation(self):

        """
        Метод для валидации данных полученных
        из метода add_vacancies_file. Переводит
        мнимальную, максимальную и среднню
        заработную плату в рубли, если
        изначальнные данные поступили в USD
        """

        # rate = get_currency_rate()
        rate = 99.04
        data = self.add_vacancies_file()
        self.validate_vacancy = []
        for i in data:
            self.dict_validate = dict()
            self.dict_validate['job_title'] = i['job_title']
            self.dict_validate['location'] = i['location']
            self.dict_validate['employer'] = i['employer']
            self.dict_validate['url'] = i['url']
            self.dict_validate['requirement'] = i['requirement']
            self.dict_validate['responsibilities'] = i['responsibilities']
            if i['currency'] == 'USD':
                self.dict_validate['salary_min'] = int(i['salary_min']) * rate
                self.dict_validate['salary_max'] = int(i['salary_max']) * rate
                self.dict_validate['salary_average'] = int(i['salary_average']) * rate
                self.dict_validate['currency'] = 'RUR'
            else:
                self.dict_validate['salary_min'] = int(i['salary_min'])
                self.dict_validate['salary_max'] = int(i['salary_max'])
                self.dict_validate['salary_average'] = int(i['salary_average'])
                self.dict_validate['currency'] = i['currency']
            self.validate_vacancy.append(self.dict_validate)
        return self.validate_vacancy

    def sort_data_of_salary(self):

        all_data = self.validation()
        salary_sort = sorted(all_data, key=lambda data: data['salary_average'], reverse=True)
        if self.request_salary.lower() == 'по убыванию':
            return salary_sort
        elif self.request_salary.lower() == 'по возрастанию':
            salary_sort = sorted(all_data, key=lambda data: data['salary_average'], reverse=False)
            return salary_sort
        else:
            return all_data

    def get_information(self, user_request):
        """"
        Метод для получения данных из файла по указанным критериям
        и вывода данных в консоль для удобаства пользователя.
        """
        sort_data = []
        self.user_request = user_request
        for num in self.sort_data_of_salary():
            if (self.user_request.lower() == 'job_title' or self.user_request.lower() == 'employer'
                    or self.user_request.lower() == 'url'):
                data = f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: {num['url']}\n"
                sort_data.append(data)
            elif self.user_request.lower() == 'location':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nЛокация: {num['location']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'requirement':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nТребования: {num['requirement']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'responsibilities':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nОбязанности: {num['responsibilities']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'salary_min':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nЗаработная плата от: {num['salary_min']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'salary_max':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nЗаработная плата до: {num['salary_max']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'salary_average':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nСредняя заработная плата: {num['salary_average']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'currency':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии:"
                        f" {num['url']}\nВалюта: {num['currency']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'all_data':
                data = (
                    f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: {num['url']}\n"
                    f"Локация: {num['location']}\nТребования: {num['requirement']}\nОбязанности:"
                    f" {num['responsibilities']}\nЗаработная плата от: {num['salary_min']}\n"
                    f"Заработная плата до: {num['salary_max']}\nСредняя заработная плата: {num['salary_average']}\n"
                    f"Валюта: {num['currency']}\n")
                sort_data.append(data)

        return sort_data


class JSONSaver(Vacancies):
    def __init__(self, vacansy_name: str, region: int, page_number: int, count_per_page: int, request_salary: str):
        super().__init__(vacansy_name, region, page_number, count_per_page, request_salary)

    def save_json(self, data):
        """Метод для сохранения json файла."""
        with open('../superjob_hh/vacancy.csv', 'w', newline='', encoding='utf8') as file:
            new_file = file.write(json.dumps(data, indent=2, ensure_ascii=False))
            return new_file

    #
    def save_sort_txt(self):
        """Метод для сохранения отсортированных данных в .txt."""
        data = self.get_information(self.user_request)
        with open("sort_data.txt", "w") as file:
            for d in data:
                file.write(d.replace('[', '').replace(']', '')
                           .replace("'", "|").replace(r"\n", ' ') + '\n')
