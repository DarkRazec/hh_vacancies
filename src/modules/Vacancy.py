from src.get_currency_rate import get_currency_rate


class Vacancy:
    """Класс для абстракции 'Вакансия'"""
    name: str
    url: str
    salary: dict
    desc: dict
    __slots__ = ('__name', '__url', '__from', '__to', '__currency', '__desc', '__requirements')

    def __init__(self, name: str, url: str, salary: dict, desc: dict[str, str]):
        self.__name = name
        self.__url = url
        self.__from, self.__to, self.__currency, _ = salary.values() if salary else (0, 0, '', None)
        self.__desc, self.__requirements = desc.values() if desc else ('', '')

    def __str__(self):
        if self.__from:
            if self.__to:
                return f"Вакансия {self.__name} с заработной платой от {self.__from} до {self.__to} {self.__currency} {self.__url}"
            return f"Вакансия {self.__name} с заработной платой {self.__from} {self.__currency} {self.__url}"
        return f"Вакансия {self.__name} c неуказанной заработной платой {self.__url}"

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def salary(self) -> tuple[int, int, str | None]:
        return self.__from, self.__to, self.__currency

    @property
    def desc(self):
        return self.__desc

    @property
    def requirements(self):
        return self.__requirements

    def get_from(self):
        if self.__from:
            return self.__from
        return 0

    def get_to(self):
        if self.__to:
            return self.__to
        return 0

    # TODO Переписать метод
    def compare_vacs(self, other: 'Vacancy') -> str:
        """
        Возвращает строку со сравнением двух вакансий по заработной плате
        :param other: Вакансия для сравнения
        :return: Строку со сравнением двух вакансий
        """
        if isinstance(other, Vacancy):
            if not (other.get_from() and self.get_from()):
                return f"У одной из вакансий не указана заработная плата"
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            this_salary = self.salary_median(this_from, this_to)
            other_salary = other.salary_median(other_from, other_to)
            if other_salary > this_salary:
                return f"На вакансии {other.name} предлагают большую зарплату"
            elif other_salary < this_salary:
                return f"На вакансии {self.__name} предлагают большую зарплату"
            return f"Обе вакансии предлагают одинаковую зарплату"
        else:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def salary_to_rub(self) -> tuple[float, float]:
        """Возвращает значения зарплаты приведенные к рублю"""
        if self.__currency != 'RUB':
            curr_rate = get_currency_rate(self.__currency)
            new_from, new_to = [curr_rate * i for i in (self.get_from(), self.get_to())]
            return new_from, new_to
        return self.get_from(), self.get_to()

    @staticmethod
    def salary_median(salary_from, salary_to) -> float:
        """Возвращает среднюю зарплату, если в аргументы передан диапазон зарплаты"""
        if salary_to:
            return (salary_from + salary_to) / 2
        return salary_from
