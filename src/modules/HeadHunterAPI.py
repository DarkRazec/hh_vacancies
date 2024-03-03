import json
import requests
from src.modules.APIVacancy import APIVacancy


class HeadHunterAPI(APIVacancy):
    """Класс для работы с API сервисом 'api.hh.ru'"""
    url: str

    def __init__(self):
        self.__url = 'https://api.hh.ru/'

    def get_vacancies(self, search_query: str, search_num: int = 10, page: int = 0, exp: str = None) -> list[dict]:
        """
        Обращается к API сервису и возвращает список вакансий
        :param search_query: Запрос пользователя
        :param search_num: Количество элементов выдачи (макс. 100)
        :param page: Номер страницы
        :param exp: Опыт работы. Принимает значения: "noExperience", "between1And3", "between3And6", "moreThan6"
        :return: Список словарей
        """
        params = {
            'text': search_query,
            'experience': exp,
            'order_by': 'publication_time',
            'per_page': search_num,
            'page': page
        }
        response = requests.get(self.__url + 'vacancies', params=params)
        response.raise_for_status()
        return json.loads(response.text)['items']
