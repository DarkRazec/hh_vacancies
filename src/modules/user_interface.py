from src.modules.hh_api import HeadHunterAPI
from src.modules.vacancy import Vacancy
from src.modules.vacancy_json import VacancyJSON
from src.json_to_vacancies import json_to_vacancies
import os


class UserInterface:
    """Класс для взаимодействия пользователя с модулями программы"""
    vacancies: list[Vacancy] = None

    def __init__(self):
        fs_mode = {
            "json": VacancyJSON,
            "sql": "TODO",
            "csv": "TODO",
            "excel": "TODO"
        }
        self.vac_fs = fs_mode["json"]()  # Других форматов пока нет, так что захардкодил
        try:
            while True:
                user_input = input("""
Введите режим работы с программой:
    1 - получить вакансии с сайта
    2 - сохранить в файл
    3 - показать данные из файла
    4 - удалить данные из файла
    5 - выйти)
    """)
                if user_input in ("5", "выйти"):
                    exit(0)
                if user_input in ('1', 'получить'):
                    self.vacancies = self.api_get()
                elif user_input in ('2', 'сохранить'):
                    if self.vacancies:
                        self.file_save()
                    else:
                        print("\nОтсутствуют вакансии для сохранения")
                elif user_input in ('3', 'показать'):
                    [print(f"\t{vacancy}") for vacancy in self.file_get()]
                elif user_input in ('4', 'удалить'):
                    self.file_delete()
        except ValueError as e:
            raise e

    @staticmethod
    def num_check(num) -> int:
        """
        Приводит переданный аргумент к целочисленному типу и возвращает полученное значение, либо возвращает 0
        :param num: Значение для проверки
        :return: Целое число
        """
        if not num:
            return 0
        try:
            return int(num)
        except ValueError:
            return 0

    def file_save(self) -> None:
        """Функция для взаимодействия с методом сохранения данных класса VacancyToFile"""
        try:
            vac_nums = [int(num) for num in input("\nВведите через пробел номера вакансий, которые хотите сохранить"
                                                  "(оставьте это поле пустым, чтобы сохранить все вакансии) ").split()]
            if vac_nums:
                vac_to_save = [self.vacancies[i - 1] for i in vac_nums if 0 < i < len(self.vacancies)]
                self.vac_fs.save_to_file(vac_to_save)
        except ValueError:
            print("\nВведено неверное значение")
            return
        else:
            self.vac_fs.save_to_file(self.vacancies)

    def file_get(self) -> list[Vacancy] | list[str]:
        """Метод для взаимодействия пользователя с методом получения данных из файла класса VacancyToFile"""
        if os.stat(self.vac_fs.path).st_size != 0:
            name = input("\n(Необязательно) Введите название вакансии для поиска файле ")
            salary = self.num_check(
                input("(Необязательно) Введите сумму зарплаты в рублях для поиска вакансии в файле "))
            json_vacancies = self.vac_fs.get_from_file(name, salary)
            (print("\nПолученный список вакансий:"))
            return json_to_vacancies(json_vacancies) if json_vacancies else ["По вашему запросу ничего не найдено"]
        else:
            return ["Файл пуст"]

    def file_delete(self) -> None:
        """Метод для взаимодействия пользователя с методом удаления данных класса VacancyToFile"""
        if os.stat(self.vac_fs.path).st_size != 0:
            user_input = input("\nВведите название вакансии, которую хотите удалить. Оставьте поле пустым, "
                               "чтобы удалить все данные из файла ")
            self.vac_fs.delete_from_file(user_input)
        else:
            print("Файл пуст")

    def api_get(self) -> list[Vacancy]:
        """Метод для взаимодействия пользователя с методом получения вакансий API класса"""
        search_query = input(
            "\nВведите ключевые слова для поиска вакансий (можно ввести название, регион, диапазон зарплат): ")
        search_num = self.num_check(input("(Необязательно) Введите количество вакансий для вывода (не более 100): "))
        search_page = self.num_check(input("(Необязательно) Введите номер страницы для вывода: "))
        hh_api = HeadHunterAPI()
        raw_vacancies = hh_api.get_vacancies(search_query, search_num, search_page)
        vacancies = [Vacancy(vacancy["name"], vacancy["alternate_url"],
                             (vacancy["salary"]["from"], vacancy["salary"]["to"], vacancy["salary"]["currency"])
                             if vacancy["salary"] else None,
                             (vacancy["area"]["name"], vacancy["employer"]["name"], vacancy["schedule"]["name"],
                              vacancy["experience"]["name"])) for vacancy in raw_vacancies]
        print("\nПолученный список вакансий:")
        [print(f"\t{i + 1}:\t", vacancies[i]) for i in range(len(vacancies))]
        return vacancies
