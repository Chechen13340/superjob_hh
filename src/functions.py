from superjob_hh.src.HH_parser import Vacancies, JSONSaver


def user_get_data():
    """
    Функция для получения информации по API
    и сортировки данных по заработной плате
    возвращает экземпляр класса JSONSaver
    """
    user_vacansy = input('Введите название вакансии ')
    user_area = int(input('Введите интересующий вас регион (номер 113 - поиск по всей России) '))
    user_page = int(input('Введите номер страницы поиска  (начинается с нулевой) '))
    user_count_per_page = int(input('Количество объявлений на странице '))

    request_salary = input(
        'Отсортировать список вакансий по средней заработной плате ("По убыванию"/"По возрастанию")? ')
    hh = Vacancies(user_vacansy, user_area, user_page, user_count_per_page, request_salary)
    hh.sort_data_of_salary()
    json_saver = JSONSaver(user_vacansy, user_area, user_page, user_count_per_page, request_salary)
    json_saver.save_json(hh.sort_data_of_salary())
    return json_saver


def user_sort():
    """
    Функция для сортировки списка вакансий по ключу словаря.
    Выводит отсортированную по зарплате информацию по ключу словаря.
    """
    json_saver = user_get_data()
    user_request = input('Введите информацию для сортировки:(job_title, location, employer, url, requirement, '
                         'responsibilities,  salary_min, salary_max, salary_average, currency, all_data)'
                         ' для завершения введите "Выход" ')
    information = json_saver.get_information(user_request)
    while user_request != 'Выход':
        information = json_saver.get_information(user_request)
        user_request = input('Введите информацию для сортировки:(job_title, location, employer, url, requirement, '
                             'responsibilities,  salary_min, salary_max, salary_average, currency, all_data)'
                             ' для завершения введите "Выход" ')
    json_saver.save_sort_txt()
    for info in information:
        print(info)
    return json_saver


def del_info():
    """
    Функция для удаления информации по ключу
     из словаря. Возвращает отсортированные,
     в том числе после удаления, данные в txt файл.
    """
    json_saver = user_sort()
    user_key = input('Введите ключевое слово чтобы удалить ненужные данные (для завершения введите "Выход" ): ')
    json_saver.del_data(user_key)
    while user_key != 'Выход':
        json_saver.del_data(user_key)
        user_key = input('Введите ключевое слово чтобы удалить ненужные данные (для завершения введите "Выход"): ')
    return json_saver.save_sort_txt()
