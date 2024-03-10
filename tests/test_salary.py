from src.modules.salary import Salary
from src.get_currency_rate import get_currency_rate


def test_salary():
    salary = Salary((None, None, 'RUR'))
    assert salary.get_to() == 0
    assert salary.get_from() == 0
    assert salary.currency == 'RUR'
    assert salary.salary == (0, 0, 'RUR')


def test_salary_to_rub():
    salary_1 = Salary((1, 2, 'RUR'))
    assert salary_1.salary_to_rub() == [1, 2]
    salary_2 = Salary((1, 2, 'USD'))
    assert salary_2.salary_to_rub() == [get_currency_rate('usd') * num for num in [1, 2]]


def test_salary_median():
    salary_1 = Salary((1, None, 'RUR'))
    assert salary_1.salary_median() == 1
    salary_2 = Salary((2, 4, 'RUR'))
    assert salary_2.salary_median() == 3
