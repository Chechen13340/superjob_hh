from abc import abstractmethod, ABC


class HH_SJ_API(ABC):
    def __init__(self, url: str, headers: dict, params: dict):
        self.url = url
        self.headers = headers
        self.params = params

    @abstractmethod
    def get_data(self) -> dict:
        """
        Абстрактный метод для получения данных
        через API в виде словаря.
        """
        pass

    @abstractmethod
    def add_vacancies_file(self):
        """"
        Метод для добавления информауии о вакансиях в список
        словарей для последующей записи json файла.
        """
        pass

    @abstractmethod
    def get_information(self, information: str):
        """"
        Метод для получения данных из файла по указанным критериям
        и вывода данных в консоль для удобаства пользователя.
        """
        pass

    @abstractmethod
    def del_data(self, key_word: str):
        """"
        Метод для удаления определенных данных,
        которые не нужны пользователю из файла.
        """
        pass
