from src.get_currency_rate import get_currency_rate


class Vacancy:
    """Класс для абстракции 'Вакансия'"""
    name: str
    url: str
    __from: int
    __to: int
    currency: str
    area: str
    company: str
    schedule: str
    exp: str
    __slots__ = ('__name', '__url', '__from', '__to', '__currency', '__area', '__company', '__schedule', '__exp')

    def __init__(self, name: str, url: str, salary: tuple, desc: tuple):
        self.__name = name
        self.__url = url
        self.__from, self.__to, self.__currency = salary if salary else (0, 0, 'RUR')
        self.__area, self.__company,  self.__schedule, self.__exp = desc if desc else (None, None, None, None)

    def __str__(self):
        if self.__from:
            if self.__to:
                return f"Вакансия {self.__name} с заработной платой от {self.__from} до {self.__to} {self.__currency} {self.__url}"
            return f"Вакансия {self.__name} с заработной платой {self.__from} {self.__currency} {self.__url}"
        return f"Вакансия {self.__name} c неуказанной заработной платой {self.__url}"

    # Геттеры и Property
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
    def area(self):
        if self.__area:
            return self.__area
        return "не указано"

    @property
    def company(self):
        return self.__company

    @property
    def schedule(self):
        if self.__schedule:
            return self.__schedule
        return "не указано"

    @property
    def exp(self):
        if self.__exp:
            return self.__exp
        return "без опыта"

    @property
    def currency(self):
        return self.__currency

    @property
    def desc(self):
        return (f"Компания {self.__company} предлагает данную вакансию в городе {self.area}. "
                f"График работы: {self.schedule}. Требуемый опыт: {self.exp}")

    def get_from(self):
        if self.__from:
            return self.__from
        return 0

    def get_to(self):
        if self.__to:
            return self.__to
        return 0

    # Сравнение вакансий
    def __lt__(self, other):
        try:
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            if self.salary_median(this_from, this_to) < other.salary_median(other_from, other_to):
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __le__(self, other):
        try:
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            if self.salary_median(this_from, this_to) <= other.salary_median(other_from, other_to):
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __eq__(self, other):
        try:
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            if self.salary_median(this_from, this_to) == other.salary_median(other_from, other_to):
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __ne__(self, other):
        try:
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            if self.salary_median(this_from, this_to) != other.salary_median(other_from, other_to):
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __gt__(self, other):
        try:
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            if self.salary_median(this_from, this_to) > other.salary_median(other_from, other_to):
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __ge__(self, other):
        try:
            this_from, this_to = self.salary_to_rub()
            other_from, other_to = other.salary_to_rub()
            if self.salary_median(this_from, this_to) >= other.salary_median(other_from, other_to):
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def salary_to_rub(self) -> tuple[float, float]:
        """Возвращает значения зарплаты приведенные к рублю"""
        if self.__currency != 'RUR':
            curr_rate = get_currency_rate(self.__currency)
            new_from, new_to = [curr_rate * i for i in (self.get_from(), self.get_to())]
            return new_from, new_to
        return self.get_from(), self.get_to()

    @staticmethod
    def salary_median(salary_from, salary_to) -> float:
        """Возвращает среднюю зарплату, если в аргументы передан диапазон зарплаты"""
        if salary_to:
            return round((salary_from + salary_to) / 2)
        return salary_from
