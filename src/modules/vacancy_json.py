from src.modules.vacancies_to_file import VacanciesToFile
import json
import os
from src.get_currency_rate import get_currency_rate
from src.vacancies_to_json import vacancies_to_json
from src.json_to_vacancies import json_to_vacancies


def is_salary_in(sal: int, sal_to_compare: dict) -> bool:
    """
    Проверяет, находится ли переданное значение зарплаты в переданном диапазоне зарплат
    :param sal: проверяемое значение зарплаты
    :param sal_to_compare: диапазон зарплат
    """
    if sal_to_compare["currency"] != "RUR":
        sal = round(sal / get_currency_rate(sal_to_compare["currency"].lower()))
    if sal_to_compare["from"] <= sal <= sal_to_compare["to"]:
        return True
    return False


class VacancyJSON(VacanciesToFile):
    """Класс для взаимодействия объектов класса Vacancy с JSON файлами"""

    def __init__(self, path: str = "data/vacancies.json"):
        super().__init__(path)
        self.__path = os.path.abspath(path)

    @property
    def path(self):
        if self.__path:
            return self.__path
        else:
            raise ValueError("Путь к файлу не указан")

    def save_to_file(self, vacancies: list):
        try:
            # Загрузка данных в файл JSON (или его создание, если такого файла нет)
            if os.stat(self.path).st_size == 0:
                with open(self.path, 'w', encoding='UTF-8') as f:
                    json.dump(vacancies_to_json(vacancies), f, indent=4, ensure_ascii=False)
            else:
                with open(self.path, 'r+', encoding='UTF-8') as f:
                    vac_list = json_to_vacancies(json.load(f))
                    [vac_list.append(vacancy) for vacancy in vacancies]
                    f.seek(0)
                    json.dump(vacancies_to_json(vac_list), f, indent=4, ensure_ascii=False)
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def get_from_file(self, name: str = None, salary: int = None):
        with open(self.path, encoding='UTF-8') as f:
            json_list = json.load(f)
        if name:
            if salary:
                return [i for i in json_list if name in i["name"] and is_salary_in(salary, i["salary"])]
            return [i for i in json_list if name in i["name"]]
        elif salary:
            return [i for i in json_list if is_salary_in(salary, i["salary"])]
        return json_list

    def delete_from_file(self, name: str = None):
        with open(self.path, 'r+', encoding='UTF-8') as f:
            data_list = json.load(f)
        # Удаление из списка ОДНОЙ вакансии, соответствующей переданному аргументу, и запись списка обратно в файл
            if name:
                for i in data_list:
                    if name.lower() in i["name"].lower():
                        data_list.remove(i)
                        break
                f.seek(0)
                json.dump(data_list, f, indent=4, ensure_ascii=False)
                f.truncate()
            # Удаление ВСЕХ данных из файла
            else:
                user_input = input("Вы уверены, что хотите удалить ВСЕ данные из файла?(Y/n) ")
                if user_input in ('y', 'да'):
                    f.truncate(0)  # Стирает все данные из файла
                else:
                    print("Удаление данных прервано")
