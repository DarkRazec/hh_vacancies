import pytest
from src.modules.Vacancy import Vacancy


def test_vacancy():
    vac = Vacancy('TEST', 'TEST', {'from': 1, 'to': 2, 'currency': 'RUB', '': ''}, {'T': 'E', 'S': 'T'})
    assert vac.name == 'TEST'
    assert vac.salary == (1, 2, 'RUB')
    assert vac.__str__() == "Вакансия TEST с заработной платой от 1 до 2 RUB TEST"


def test_compare():
    vac_1 = Vacancy('TEST', 'TEST', {'from': 10000, 'to': 60000, 'currency': 'RUB', '': ''}, {'T': 'E', 'S': 'T'})
    vac_2 = Vacancy("TEST", 'TEST', {'from': 10000, 'to': 60000, 'currency': 'RUB', '': ''}, {'T': 'E', 'S': 'T'})
    assert vac_1.compare_vacs(vac_2) == 'Обе вакансии предлагают одинаковую зарплату'
    vac_3 = Vacancy('TEST3', 'TEST', {'from': 100000, 'to': None, 'currency': 'USD', '': ''}, {'T': 'E', 'S': 'T'})
    assert vac_2.compare_vacs(vac_3)
    vac_4 = Vacancy('TEST4', 'TEST', {'from': 30000, 'to': 100000, 'currency': 'RUB', '': ''}, {'T': 'E', 'S': 'T'})
    assert vac_3.compare_vacs(vac_4) == "На вакансии TEST3 предлагают большую зарплату"
    assert vac_4.compare_vacs(vac_3) == "На вакансии TEST3 предлагают большую зарплату"
    with pytest.raises(TypeError):
        assert vac_4.compare_vacs('TEST')
    vac_5 = Vacancy('TEST4', 'TEST', {'from': None, 'to': None, 'currency': '', '': ''}, {'T': 'E', 'S': 'T'})
    assert vac_4.compare_vacs(vac_5) == 'У одной из вакансий не указана заработная плата'


def test_salary_median():
    assert Vacancy.salary_median(1, None) == 1
    assert Vacancy.salary_median(1, 2) == 1.5


def test_salary_to_rub():
    vac_1 = Vacancy('TEST', 'TEST', {'from': 1, 'to': None, 'currency': 'RUB', '': ''}, {'T': 'E', 'S': 'T'})
    assert vac_1.salary_to_rub() == (1, 0)
    vac_2 = Vacancy('TEST', 'TEST', {'from': None, 'to': 1, 'currency': 'USD', '': ''}, {'T': 'E', 'S': 'T'})
    assert type(vac_2.salary_to_rub()) is tuple
