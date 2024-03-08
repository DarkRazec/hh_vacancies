def vacancies_to_json(vacancies: list) -> list[dict]:
    """
    Возвращает список вакансий в формате JSON
    :param vacancies: список объектов класса Vacancy
    :return: список вакансий в формате JSON
    """
    json_vacancies = []
    for vacancy in vacancies:
        vac_json = {
            "name": vacancy.name,
            "desc": {"area": vacancy.area, "company": vacancy.company, "schedule": vacancy.schedule,
                     "exp": vacancy.exp},
            "salary": {"from": vacancy.get_from(), "to": vacancy.get_to(), "currency": vacancy.currency},
            "url": vacancy.url
        }
        json_vacancies.append(vac_json)
    return json_vacancies
