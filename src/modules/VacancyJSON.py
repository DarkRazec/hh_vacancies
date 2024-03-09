from src.modules.VacanciesToFile import VacanciesToFile
import json
import os
from src.get_currency_rate import get_currency_rate
from src.vacancies_to_json import vacancies_to_json
from src.json_to_vacancies import json_to_vacancies


def is_salary_in(sal: int, sal_to_compare: dict) -> bool:
    """
    Проверяет, находится ли переданное значение зарплаты в переданном диапазоне зарплат
    :param sal:
    :param sal_to_compare:
    :return:
    """
    if sal_to_compare["currency"] != "RUR":
        sal = round(sal / get_currency_rate(sal_to_compare["currency"]))
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

    def save_to_file(self, vacancies):
        try:
            # Загрузка данных в файл JSON (или его создание, если такого файла нет)
            with open(self.path, 'a', encoding='UTF-8') as f:
                if os.stat(self.path).st_size == 0:
                    json.dump(vacancies_to_json(vacancies), f, indent=4, ensure_ascii=False)
                else:
                    with open(self.path, encoding='UTF-8') as old_f:
                        vac_list = json_to_vacancies(json.load(old_f))
                        [vac_list.append(vacancy) for vacancy in vacancies]
                        vac_list.sort(reverse=True)
                    with open(self.path, 'w', encoding='UTF-8') as new_f:
                        json.dump(vacancies_to_json(vac_list), new_f, indent=4, ensure_ascii=False)
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def get_from_file(self, name: str = None, salary: int = None):
        with open(self.path, encoding='UTF-8') as f:
            json_list = json.load(f)
        vac_to_return = []
        if name:
            if salary:
                for i in json_list:
                    if name in i["name"]:
                        if is_salary_in(salary, i["salary"]):
                            vac_to_return.append(i)
                return vac_to_return
            return [i for i in json_list if name in i["name"]]
        elif salary:
            for i in json_list:
                if is_salary_in(salary, i["salary"]):
                    vac_to_return.append(i)
            return vac_to_return
        return json_list

    def delete_from_file(self, name: str = None):
        with open(self.path, encoding='UTF-8') as f:
            data_list = json.load(f)
        # Удаление из списка ОДНОЙ вакансии, соответствующей переданному аргументу, и запись списка обратно в файл
        if name:
            for i in data_list:
                if name in i["name"]:
                    data_list.remove(i)
                    break
            with open(self.path, 'w', encoding='UTF-8') as new_f:
                json.dump(data_list, new_f, indent=4, ensure_ascii=False)
        # Удаление ВСЕХ данных из файла
        else:
            user_input = input("Вы уверены, что хотите удалить ВСЕ данные из файла?(Y/n) ")
            if user_input in ('y', 'да'):
                with open(self.path, 'w'):  # Стирает все данные из файла
                    return
            else:
                print("Удаление данных прервано")
                return
