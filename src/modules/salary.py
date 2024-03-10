from src.get_currency_rate import get_currency_rate


class Salary:
    """Класс для абстракции 'Заработная плата'"""
    __from: int
    __to: int
    __currency: str
    __slots__ = ('__from', '__to', '__currency')

    def __init__(self, salary: tuple):
        self.__from = salary[0] if salary and salary[0] else 0
        self.__to = salary[1] if salary and salary[1] else 0
        self.__currency = salary[2] if salary and salary[2] else 'RUR'

    def get_from(self) -> int:
        return self.__from

    def get_to(self) -> int:
        return self.__to

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def salary(self) -> tuple[int, int, str | None]:
        return self.__from, self.__to, self.__currency

    def salary_to_rub(self) -> list[float | int]:
        """Возвращает значения зарплаты приведенные к рублю"""
        if self.__currency != "RUR":
            curr_rate = get_currency_rate(self.__currency.lower())
            return [curr_rate * i for i in (self.__from, self.__to)]
        return [self.__from, self.__to]

    def salary_median(self) -> int:
        """Возвращает среднюю зарплату, если в аргументы передан диапазон зарплаты"""
        new_from, new_to = self.salary_to_rub()
        if new_to:
            return round((new_from + new_to) / 2)
        return new_from

    # Сравнение вакансий
    def __lt__(self, other) -> bool:
        try:
            if self.salary_median() < other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __le__(self, other) -> bool:
        try:
            if self.salary_median() <= other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __eq__(self, other) -> bool:
        try:
            if self.salary_median() == other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __ne__(self, other) -> bool:
        try:
            if self.salary_median() != other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __gt__(self, other) -> bool:
        try:
            if self.salary_median() > other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __ge__(self, other) -> bool:
        try:
            if self.salary_median() >= other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")
