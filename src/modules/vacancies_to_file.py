from abc import ABC, abstractmethod
from src.modules.vacancy import Vacancy


class VacanciesToFile(ABC):
    """Абстрактный класс для взаимодействия объектов класса Vacancy с файлами"""
    path: str

    def __init__(self, path: str):
        self.__path = path

    @abstractmethod
    def save_to_file(self, *vacancy: Vacancy) -> None:
        """
        Сохраняет вакансию в файл
        :param vacancy: Вакансии для сохранения в файл
        """
        pass

    @abstractmethod
    def get_from_file(self, name: str = None, salary: int = None) -> list[dict]:
        """
        Возвращает вакансию с указанными критериями или список всех вакансий, если критериев нет
        :param name: Критерий поиска вакансии по названию
        :param salary: Критерий поиска вакансии по зарплате
        :return: Вакансию или список вакансий
        """
        pass

    @abstractmethod
    def delete_from_file(self, name: str = None) -> None:
        """
        Удаляет вакансию с указанными критериями или все вакансии, если критериев нет
        :param name: Критерий поиска вакансии по названию
        """
        pass
