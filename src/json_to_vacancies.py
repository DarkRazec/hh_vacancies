from src.modules.Vacancy import Vacancy


def json_to_vacancies(raw_vacancies) -> list[Vacancy]:
    """
    Возвращает список объектов класса Vacancy, сформированных из JSON формата
    :param raw_vacancies: список вакансий в формате JSON
    :return: Список объектов Vacancy
    """
    return [Vacancy(vacancy["name"], vacancy["url"], vacancy["salary"].values(),
                    vacancy["desc"].values()) for vacancy in raw_vacancies]
