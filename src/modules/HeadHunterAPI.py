import json

from src.modules.APIVacancy import APIVacancy
import requests


class HeadHunterAPI(APIVacancy):
    """Класс для работы с API сервисом 'api.hh.ru'"""

    def __init__(self):
        self.__url = 'https://api.hh.ru/'

    def get_vacancies(self, search_query: str, search_num: int = 10) -> list[dict]:
        response = requests.get(self.__url + f"vacancies/?text={search_query}" + f"&&per_page={search_num}")
        response.raise_for_status()
        return json.loads(response.text)['items']
