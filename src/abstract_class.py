from abc import abstractmethod, ABC


class HH_SJ_API(ABC):
    def __init__(self, url: str, headers: dict, params: dict):
        self.url = url
        self.headers = headers
        self.params = params

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def save_json(self):
        pass
