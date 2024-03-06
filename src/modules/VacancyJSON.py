from src.modules.VacanciesToFile import VacanciesToFile
import json
import os
from src.get_currency_rate import get_currency_rate


class VacancyJSON(VacanciesToFile):
    """Класс для взаимодействия объектов класса Vacancy с JSON файлами"""

    def __init__(self, path: str = "../../data/vacancies.json"):
        super().__init__(path)

    def save_to_file(self, *vacancies):
        try:
            for vacancy in vacancies:
                # Приведение данных из переданной вакансии к формату JSON
                vac_to_json = {
                    "name": vacancy.name,
                    "desc": vacancy.desc,
                    "requirements": vacancy.requirements,
                    "salary": {"from": vacancy.get_from(), "to": vacancy.get_to(), "currency": vacancy.currency},
                    "url": vacancy.url
                }
                # Загрузка данных в файл JSON (или его создание, если такого файла нет)
                with open(self._path, 'a', encoding='UTF-8') as f:
                    if os.stat(self._path).st_size == 0:
                        json.dump([vac_to_json], f, indent=4)
                    else:
                        with open(self._path, encoding='UTF-8') as old_f:
                            data_list = json.load(old_f)
                            data_list.append(vac_to_json)
                        with open(self._path, 'w', encoding='UTF-8') as new_f:
                            json.dump(data_list, new_f, indent=4)
        except AttributeError:
            raise TypeError("Переданный аргумент не является объектом класса Vacancy")

    def get_from_file(self, name: str = None, salary: int = None):
        with open(self._path, encoding='UTF-8') as f:
            data_list = json.load(f)
        if name:
            if salary:
                vac_to_return = []
                for i in data_list:
                    if name in i["name"]:
                        sal_to_check = salary
                        if i["salary"]["currency"] != "RUB":
                            sal_to_check = round(sal_to_check / get_currency_rate(i["salary"]["currency"]))
                        if sal_to_check in range(i["salary"]["from"], i["salary"]["to"]):
                            vac_to_return.append(i)
                return vac_to_return
            return [i for i in data_list if name in i["name"]]
        return data_list

    def delete_from_file(self, name: str = None):
        with open(self._path, encoding='UTF-8') as f:
            data_list = json.load(f)
        # Удаление из списка ОДНОЙ вакансии, соответствующей переданному аргументу, и запись списка обратно в файл
        if name:
            for i in data_list:
                if name in i["name"]:
                    data_list.remove(i)
                    break
            with open(self._path, 'w', encoding='UTF-8') as new_f:
                json.dump(data_list, new_f, indent=4)
        # Удаление ВСЕХ данных из файла
        else:
            user_input = input("Вы уверены, что хотите удалить ВСЕ данные из файла?(Y/n) ")
            if user_input in ('y', 'да'):
                with open(self._path, 'w'):  # Стирает данные из файла
                    return
            else:
                print("Удаление данных прервано")
                return
