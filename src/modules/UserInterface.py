from src.modules.HeadHunterAPI import HeadHunterAPI
from src.modules.Vacancy import Vacancy
from src.modules.VacancyJSON import VacancyJSON
from src.json_to_vacancies import json_to_vacancies
import os


class UserInterface:
    """Класс для взаимодействия пользователя с модулями программы"""
    vacancies: list[Vacancy] = None

    def __init__(self):
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
                fs_mode = {
                    "json": VacancyJSON,
                    "sql": "TODO",
                    "csv": "TODO",
                    "excel": "TODO"
                }
                self.vac_fs = fs_mode["json"]()  # Других форматов пока нет, так что захардкодил
                if user_input in ('1', 'получить'):
                    print("")
                    self.vacancies = self.api_get()
                elif user_input in ('2', 'сохранить'):
                    print("")
                    if self.vacancies:
                        self.file_save()
                    else:
                        print("\nОтсутствуют вакансии для сохранения")
                elif user_input in ('3', 'показать'):
                    print("")
                    [print(vacancy) for vacancy in self.file_get()]
                elif user_input in ('4', 'удалить'):
                    print("")
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
        vac_nums = [int(num) for num in input("Введите через пробел номера вакансий, которые хотите сохранить"
                                              "(оставьте это поле пустым, чтобы сохранить все вакансии) ").split()]
        if vac_nums:
            vac_to_save = [self.vacancies[i] for i in range(len(self.vacancies)) if i + 1 in vac_nums]
            self.vac_fs.save_to_file(vac_to_save)
        else:
            self.vac_fs.save_to_file(self.vacancies)

    def file_get(self) -> list[Vacancy] | list[str]:
        """Метод для взаимодействия пользователя с методом получения данных из файла класса VacancyToFile"""
        if os.stat(self.vac_fs.path).st_size != 0:
            name = input("(Необязательно) Введите название вакансии для поиска файле ")
            salary = self.num_check(input("(Необязательно) Введите зарплату для поиска вакансии в файле "))
            print("")
            json_vacancies = self.vac_fs.get_from_file(name, salary) if True else None
            return json_to_vacancies(json_vacancies) if json_vacancies else ["По вашему запросу ничего не найдено"]
        else:
            return ["Файл пуст"]

    def file_delete(self) -> None:
        """Метод для взаимодействия пользователя с методом удаления данных класса VacancyToFile"""
        if os.stat(self.vac_fs.path).st_size != 0:
            user_input = input("Введите название вакансии, которую хотите удалить. Оставьте поле пустым, чтобы удалить "
                               "все данные из файла ")
            self.vac_fs.delete_from_file(user_input)
        else:
            print("Файл пуст")

    def api_get(self) -> list[Vacancy]:
        """Метод для взаимодействия пользователя с методом получения вакансий API класса"""
        search_query = input(
            "Введите ключевые слова для поиска вакансий (можно ввести название, регион, диапазон зарплат): ")
        search_num = self.num_check(input("(Необязательно) Введите количество вакансий для вывода (не более 100): "))
        search_page = self.num_check(input("(Необязательно) Введите номер страницы для вывода: "))
        print("")
        hh_api = HeadHunterAPI()
        raw_vacancies = hh_api.get_vacancies(search_query, search_num, search_page)
        vacancies = [Vacancy(vacancy["name"], vacancy["alternate_url"],
                             (vacancy["salary"]["from"], vacancy["salary"]["to"], vacancy["salary"]["currency"])
                             if vacancy["salary"] else None,
                             (vacancy["area"]["name"], vacancy["employer"]["name"], vacancy["schedule"]["name"],
                              vacancy["experience"]["name"])) for vacancy in raw_vacancies]
        vacancies.sort(reverse=True)
        print("Полученный список вакансий:")
        [print(f"{i + 1}: ", vacancies[i]) for i in range(len(vacancies))]
        return vacancies
