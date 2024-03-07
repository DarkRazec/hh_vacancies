import pytest
from src.modules.Vacancy import Vacancy


def test_vacancy():
    vac = Vacancy('TEST', 'TEST', (1, 2, 'RUR'), ('T', 'E', 'S', 'T'))
    assert vac.name == 'TEST'
    assert vac.url == 'TEST'
    assert vac.salary == (1, 2, 'RUR')
    assert vac.__str__() == "Вакансия TEST с заработной платой от 1 до 2 RUR TEST"
    assert vac.currency == 'RUR'
    assert vac.area == 'T'
    assert vac.company == 'E'
    assert vac.schedule == 'S'
    assert vac.exp == 'T'
    assert vac.desc == "Компания E предлагает данную вакансию в городе T. График работы: S. Требуемый опыт: T"


def test_compare():
    vac_1 = Vacancy('TEST', 'TEST', (10000, 60000, 'RUR'), ('T', 'E', 'S', 'T'))
    vac_2 = Vacancy("TEST2", 'TEST', (10000, 60000, 'RUR'), ('T', 'E', 'S', 'T'))
    assert (vac_1 == vac_2) is True
    vac_3 = Vacancy('TEST3', 'TEST', (10000, None, 'USD'), ('T', 'E', 'S', 'T'))
    assert (vac_2 > vac_3) is False
    vac_4 = Vacancy('TEST4', 'TEST', (30000, 100000, 'RUR'), ('T', 'E', 'S', 'T'))
    assert (vac_3 != vac_4) is True
    assert (vac_4 <= vac_4) is True


def test_salary_median():
    assert Vacancy.salary_median(1, None) == 1
    assert Vacancy.salary_median(2, 5) == 4


def test_salary_to_rub():
    vac_1 = Vacancy('TEST', 'TEST', (1, None, 'RUR'), ('T', 'E', 'S', 'T'))
    assert vac_1.salary_to_rub() == (1, 0)
    vac_2 = Vacancy('TEST', 'TEST', (None, 1, 'RUR'), ('T', 'E', 'S', 'T'))
    assert type(vac_2.salary_to_rub()) is tuple
