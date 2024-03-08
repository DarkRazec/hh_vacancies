from src.modules.Salary import Salary


class Vacancy(Salary):
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
        super().__init__(salary)
        self.__name = name
        self.__url = url
        self.__area, self.__company,  self.__schedule, self.__exp = desc if desc else (None, None, None, None)

    def __str__(self):
        if self.get_from():
            if self.get_to():
                return f"Вакансия {self.__name} с заработной платой от {self.get_from()} до {self.get_to()} {self.currency} {self.__url}"
            return f"Вакансия {self.__name} с заработной платой {self.get_from()} {self.currency} {self.__url}"
        return f"Вакансия {self.__name} c неуказанной заработной платой {self.__url}"

    # Геттеры и Property
    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

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
    def desc(self):
        return (f"Компания {self.__company} предлагает данную вакансию в городе {self.area}. "
                f"График работы: {self.schedule}. Требуемый опыт: {self.exp}")

    # Сравнение вакансий
    def __lt__(self, other):
        try:
            if self.salary_median() < other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __le__(self, other):
        try:
            if self.salary_median() <= other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __eq__(self, other):
        try:
            if self.salary_median() == other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __ne__(self, other):
        try:
            if self.salary_median() != other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __gt__(self, other):
        try:
            if self.salary_median() > other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def __ge__(self, other):
        try:
            if self.salary_median() >= other.salary_median():
                return True
            return False
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")


