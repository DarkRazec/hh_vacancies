from abc import ABC, abstractmethod


class APIVacancy(ABC):
    """Абстрактный класс для работы с API сервисами, предоставляющим данные по вакансиям"""

    @abstractmethod
    def get_vacancies(self, search_query: str):
        """Обращается к API сервису и возвращает список вакансий"""
        pass
