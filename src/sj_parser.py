import json
import os

import requests

from superjob_hh.settings import SJ_API_URL
from superjob_hh.src.abstract_class import HH_SJ_API


class SJparser(HH_SJ_API):
    SJ_API_KEY = os.getenv('SJ_API_KEY')

    def __init__(self, vacancy_name: str, page_number: int, count_per_page: int):
        self.user_data = None
        self.__vacancy_name = vacancy_name
        self.__page_number = page_number
        self.__count_per_page = count_per_page
        super().__init__(url=SJ_API_URL, headers={"X-Api-App-Id": self.SJ_API_KEY}, params={
            'keyword': vacancy_name,
            'count': count_per_page,
            'page': page_number
        })

    def get_data(self) -> dict:
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data = response.json()
        return data['objects']

    def add_vacancies_file(self):
        vacancy = []
        for item in self.get_data():
            self.user_data = dict()
            self.user_data['job_title'] = item['profession']
            self.user_data['location'] = item['address']
            if item['client'].get('title') is None:
                self.user_data['employer'] = "Информация отсутствует"
                self.user_data['url'] = item['link']
                self.user_data['education'] = item['education']['title']
                self.user_data['experience'] = item['experience']['title']
                self.user_data['description'] = item['candidat']
            else:
                self.user_data['employer'] = item['client']['title']
                self.user_data['url'] = item['link']
                self.user_data['education'] = item['education']['title']
                self.user_data['experience'] = item['experience']['title']
                self.user_data['description'] = item['candidat']
            if item['payment_from'] == 0:
                self.user_data['salary_min'] = int(item['payment_from'])
                self.user_data['salary_max'] = int(item['payment_to'])
                self.user_data['salary_average'] = int(item['payment_to'])
                self.user_data['currency'] = item['currency']
            elif item['payment_to'] == 0:
                self.user_data['salary_min'] = int(item['payment_from'])
                self.user_data['salary_max'] = int(item['payment_to'])
                self.user_data['salary_average'] = int(item['payment_from'])
                self.user_data['currency'] = item['currency']
            else:
                self.user_data['salary_min'] = int(item['payment_from'])
                self.user_data['salary_max'] = int(item['payment_to'])
                self.user_data['salary_average'] = int((item['payment_from'] + item['payment_to']) // 2)
                self.user_data['currency'] = item['currency']
            vacancy.append(self.user_data)

        return vacancy

    def del_data(self, key_word: str):
        """"
        Метод для удаления определенных данных
        из файла .txt, которые не нужны пользователю.
        """
        self.key_word = key_word
        with open("sort_data_sj.txt") as file, open("del_data_sj.txt", 'w') as new_file:
            for line in file:
                if key_word not in line:
                    new_file.write(line)
            return new_file

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
            elif self.user_request.lower() == 'education':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nОбразование: {num['education']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'experience':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nОпыт работы: {num['experience']}\n")
                sort_data.append(data)
            elif self.user_request.lower() == 'description':
                data = (f"\nДолжность: {num['job_title']}\nРаботадатель: {num['employer']}\nСайт вакансии: "
                        f"{num['url']}\nОписание вакансии: {num['description']}\n")
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
                    f"Локация: {num['location']}\nОбразование: {num['education']}\nОпыт работы:"
                    f" {num['experience']}\nОписание вакансии: {num['description']}\nЗаработная плата от: "
                    f"{num['salary_min']}\nЗаработная плата до: {num['salary_max']}\nСредняя заработная плата:"
                    f" {num['salary_average']}\nВалюта: {num['currency']}\n")
                sort_data.append(data)

        return sort_data


class VacanciesSJ(SJparser):
    def __init__(self, vacancy_name: str, page_number: int, count_per_page: int, request_salary: str):
        self.request_salary = request_salary
        super().__init__(vacancy_name, page_number, count_per_page)

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
            self.dict_validate['education'] = i['education']
            self.dict_validate['experience'] = i['experience']
            self.dict_validate['description'] = i['description']
            if i['currency'] == 'USD' or i['currency'] == 'usd':
                self.dict_validate['salary_min'] = int(i['salary_min']) * rate
                self.dict_validate['salary_max'] = int(i['salary_max']) * rate
                self.dict_validate['salary_average'] = int(i['salary_average']) * rate
                self.dict_validate['currency'] = 'rub'
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


class JSONSaverSJ(VacanciesSJ):
    def __init__(self, vacancy_name: str, page_number: int, count_per_page: int, request_salary: str):
        super().__init__(vacancy_name, page_number, count_per_page, request_salary)

    def save_json(self, data):
        """Метод для сохранения json файла."""
        with open('../superjob_hh/vacancy_sj.csv', 'w', newline='', encoding='utf8') as file:
            new_file = file.write(json.dumps(data, indent=2, ensure_ascii=False))
            return new_file

    def save_sort_txt(self):
        """Метод для сохранения отсортированных данных в .txt."""
        data = self.get_information(self.user_request)
        with open("sort_data_sj.txt", "w") as file:
            for d in data:
                file.write(d.replace('[', '').replace(']', '')
                           .replace("'", "|").replace(r"\n", ' ') + '\n')
