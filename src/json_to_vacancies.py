from src.modules.Vacancy import Vacancy


def json_to_vacancies(raw_vacancies):
    return [Vacancy(vacancy["name"], vacancy["url"], vacancy["salary"].values(),
                    vacancy["desc"].values()) for vacancy in raw_vacancies]
