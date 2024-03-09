from src.get_currency_rate import get_currency_rate


class Salary:
    """Класс для абстракции 'Заработная плата'"""
    __from: int
    __to: int
    __currency: str
    __slots__ = ('__from', '__to', '__currency')

    def __init__(self, salary: tuple):
        self.__from, self.__to, self.__currency = salary if salary else (0, 0, 'RUR')

    def get_from(self) -> int:
        """Возвращает поле from, либо 0"""
        if self.__from:
            return self.__from
        return 0

    def get_to(self) -> int:
        """Возвращает поле to, либо 0"""
        if self.__to:
            return self.__to
        return 0

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def salary(self) -> tuple[int, int, str | None]:
        return self.__from, self.__to, self.__currency

    def salary_to_rub(self) -> list[float | int]:
        """Возвращает значения зарплаты приведенные к рублю"""
        if self.__currency != "RUR":
            curr_rate = get_currency_rate(self.__currency)
            return [curr_rate * i for i in (self.get_from(), self.get_to())]
        return [self.get_from(), self.get_to()]

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
