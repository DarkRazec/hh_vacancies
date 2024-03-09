from src.modules.Salary import Salary


class Vacancy(Salary):
    """Класс для абстракции 'Вакансия'"""
    name: str
    url: str
    area: str
    company: str
    schedule: str
    exp: str
    __slots__ = ('__name', '__url', '__area', '__company', '__schedule', '__exp')

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
    def name(self) -> str:
        return self.__name

    @property
    def url(self) -> str:
        return self.__url

    @property
    def area(self) -> str:
        if self.__area:
            return self.__area
        return "не указано"

    @property
    def company(self) -> str:
        return self.__company

    @property
    def schedule(self) -> str:
        if self.__schedule:
            return self.__schedule
        return "не указано"

    @property
    def exp(self) -> str:
        if self.__exp:
            return self.__exp
        return "без опыта"

    @property
    def desc(self) -> str:
        return (f"Компания {self.__company} предлагает данную вакансию в городе {self.area}. "
                f"График работы: {self.schedule}. Требуемый опыт: {self.exp}")
