import json

from superjob_hh.settings import OPEARTION_PATH_HH, OPEARTION_PATH_SJ
from superjob_hh.src.hh_parser import VacanciesHH, JSONSaver
from superjob_hh.src.sj_parser import VacanciesSJ, JSONSaverSJ


def user_get_data(choice_platform: str):
    """
    Функция для получения информации по API
    с плафтормы, которую выберает пользователь,
    и сортировки данных по заработной плате
    возвращает экземпляр класса JSONSaver
    """

    if choice_platform.upper() == 'HH':
        user_vacancy = input('Введите название вакансии ')
        user_area = int(input('Введите интересующий вас регион (номер 113 - поиск по всей России) '))
        user_page = int(input('Введите номер страницы поиска  (начинается с нулевой) '))
        user_count_per_page = int(input('Количество объявлений на странице '))

        request_salary = input(
            'Отсортировать список вакансий по средней заработной плате ("По убыванию"/"По возрастанию")? ')
        hh = VacanciesHH(user_vacancy, user_area, user_page, user_count_per_page, request_salary)
        hh.sort_data_of_salary()
        json_saver_hh = JSONSaver(user_vacancy, user_area, user_page, user_count_per_page, request_salary)
        json_saver_hh.save_json(hh.sort_data_of_salary())

        return json_saver_hh
    elif choice_platform.upper() == 'SJ':
        user_vacancy = input('Введите название вакансии ')
        user_page = int(input('Введите номер страницы поиска  (начинается с нулевой) '))
        user_count_per_page = int(input('Количество объявлений на странице '))

        request_salary = input(
            'Отсортировать список вакансий по средней заработной плате ("По убыванию"/"По возрастанию")? ')
        sj = VacanciesSJ(user_vacancy, user_page, user_count_per_page, request_salary)
        sj.sort_data_of_salary()
        json_saver_sj = JSONSaverSJ(user_vacancy, user_page, user_count_per_page, request_salary)
        json_saver_sj.save_json(sj.sort_data_of_salary())
        return json_saver_sj


def user_sort(choice_platform: str):
    """
    Функция для сортировки списка вакансий по ключу словаря.
    Выводит отсортированную по зарплате информацию по ключу словаря.
    """
    json_saver = user_get_data(choice_platform)
    user_request = input('Введите информацию для сортировки:\nHH(job_title, location, employer, url, requirement, '
                         'responsibilities,  salary_min, salary_max, salary_average, currency, all_data)\nSJ(job_title, '
                         'location, employer, url, education, experience, description,  salary_min, salary_max,'
                         ' salary_average, currency, all_data).\nДля завершения введите "Выход" ')
    information = json_saver.get_information(user_request)
    while user_request != 'Выход':
        information = json_saver.get_information(user_request)
        user_request = input('Введите информацию для сортировки:\nHH(job_title, location, employer, url, requirement, '
                             'responsibilities,  salary_min, salary_max, salary_average, currency, all_data)\nSJ(job_title, '
                             'location, employer, url, education, experience, description,  salary_min, salary_max,'
                             ' salary_average, currency, all_data).\nДля завершения введите "Выход" ')
    json_saver.save_sort_txt()
    for info in information:
        print(info)
    return json_saver


def del_info(choice_platform: str):
    """
    Функция для удаления информации по ключу
    из словаря. Возвращает отсортированные
    данные в txt файл.
    """
    json_saver = user_sort(choice_platform)
    user_key = input('Введите ключевое слово чтобы удалить ненужные данные (для завершения введите "Выход" ): ')
    json_saver.del_data(user_key)
    while user_key != 'Выход':
        json_saver.del_data(user_key)
        user_key = input('Введите ключевое слово чтобы удалить ненужные данные (для завершения введите "Выход"): ')
    return json_saver.save_sort_txt()


def display_top_vacncies(choice_platform: str):
    """
    Функция для вывода первых N вакансий из
    сформированного json файла после сортировки
    по заработной плате. Ничего не возвращает.
    """
    if choice_platform == 'HH':
        with open(OPEARTION_PATH_HH, 'r') as file:
            data = json.loads(file.read())
            list_data = []
            for i in data:
                dict_print = dict()
                dict_print['Должность'] = i['job_title']
                dict_print['Работодатель'] = i['employer']
                dict_print['Требования'] = i['requirement']
                dict_print['Обязанности'] = i['responsibilities']
                dict_print['Заработная плата от'] = i['salary_min']
                dict_print['Заработная плата до'] = i['salary_max']
                dict_print['Средняя заработная плата'] = i['salary_average']
                dict_print['Валюта'] = i['currency']
                list_data.append(dict_print)

            number_vacancies = int(input('Введите количество вакансий, которые Вы хотели бы вывести: '))
            for N in range(number_vacancies):
                result = '\n'.join([f'{key}: {value}' for key, value in list_data[N].items()])
                print(f'\n{result}\n')
    else:
        with open(OPEARTION_PATH_SJ, 'r') as file:
            data = json.loads(file.read())
            list_data = []
            for i in data:
                dict_print = dict()
                dict_print['Должность'] = i['job_title']
                dict_print['Работодатель'] = i['employer']
                dict_print['Сайт вакансии'] = i['url']
                dict_print['Локация'] = i['location']
                dict_print['Образование'] = i['education']
                dict_print['Опыт работы'] = i['experience']
                dict_print['Описание вакансии'] = i['description']
                dict_print['Заработная плата от'] = i['salary_min']
                dict_print['Заработная плата до'] = i['salary_max']
                dict_print['Средняя заработная плата'] = i['salary_average']
                dict_print['Валюта'] = i['currency']
                list_data.append(dict_print)

            number_vacancies = int(input('Введите количество вакансий, которые Вы хотели бы вывести: '))
            for N in range(number_vacancies):
                result = '\n'.join([f'{key}: {value}' for key, value in list_data[N].items()])
                print(f'\n{result}\n')
