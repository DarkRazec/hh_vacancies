import pytest
from src.modules.vacancy import Vacancy
from src.modules.vacancy_json import VacancyJSON
import os

path = "../hh_vacancies/tests/data/test_vacancies.json"


@pytest.fixture
def vacancy_json():
    return VacancyJSON(path)


def test_vacancy_json(vacancy_json, monkeypatch):
    vac_1 = Vacancy('TEST', 'TEST', (1, 2, 'RUR'), ('T', 'E', 'S', 'T'))
    vac_2 = Vacancy('TEST2', 'TEST2', (100, 200, 'USD'), ('T', 'E', 'S', 'T'))
    vacancy_json.save_to_file([vac_1, vac_2])
    assert vacancy_json.get_from_file('TEST')[1]['name'] == 'TEST'
    assert vacancy_json.get_from_file('TEST', 10000)[0]['name'] == 'TEST2'
    monkeypatch.setattr('builtins.input', lambda _: "y")
    vacancy_json.delete_from_file()
    assert os.stat(path).st_size == 0
