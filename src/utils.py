import re
import os


from src.classes import (JobVacancy, HHVacancyService, JSONVacancyStorage, CSVVacancyStorage, TXTVacancyStorage,
                         XLSXVacancyStorage)


def save_vacancies(vacancies: list, mode: str) -> None:
    """
    Сохраняет список вакансий в различные форматы файлов на основе выбранного режима.

    Функция запрашивает у пользователя имя файла для сохранения вакансий. В зависимости от выбранного режима ('mode'),
    вакансии сохраняются в формате JSON, CSV, TXT или XLSX. Для каждого формата используется соответствующий класс
    хранилища: JSONVacancyStorage, CSVVacancyStorage, TXTVacancyStorage, XLSXVacancyStorage. Путь к файлу формируется
    с использованием базовой директории 'data'.

    :param vacancies: список вакансий для сохранения. Каждый элемент списка является структурой данных, описывающей
                      вакансию.
    :param mode: строка, определяющая в какой формат файлов сохранять вакансии. Допустимые значения:
                 '1' - для сохранения в JSON,
                 '2' - для сохранения в CSV,
                 '3' - для сохранения в TXT,
                 '4' - для сохранения в XLSX.
    """

    user_answer = input("Введите имя файла: ")

    match int(mode):
        case 1:
            filename = os.path.join("data", user_answer + ".json")
            json_storage = JSONVacancyStorage(filename)

            for item in vacancies:
                json_storage.add_vacancy(item)
        case 2:
            filename = os.path.join("data", user_answer + ".csv")
            csv_storage = CSVVacancyStorage(filename)

            for item in vacancies:
                csv_storage.add_vacancy(item)
        case 3:
            filename = os.path.join("data", user_answer + ".txt")
            txt_storage = TXTVacancyStorage(filename)
            txt_storage.add_vacancy(vacancies)
        case 4:
            filename = os.path.join("data", user_answer + ".xlsx")
            xlsx_storage = XLSXVacancyStorage(filename)

            for item in vacancies:
                xlsx_storage.add_vacancy(item)


def get_vacancies() -> list:
    """
    Запускает процесс поиска, фильтрации и вывода на экран вакансий с использованием входных данных пользователя.

    Функция запрашивает у пользователя поисковой запрос, количество вакансий для отображения в топе, ключевые слова
    для фильтрации вакансий и диапазон зарплаты. Далее осуществляется поиск вакансий по заданным параметрам через API
    HeadHunter (HH), производится их фильтрация и сортировка. В конечном итоге на экран выводится заданное количество
    топовых вакансий, удовлетворяющих всем заданным критериям.

    :return: Полный список вакансий по критериям.
    """

    search_query = input("Введите поисковый запрос: ")
    top_count = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000 - 150000): ")

    hh_api = HHVacancyService()
    vacancies = hh_api.fetch_vacancies(search_query)
    vacancies_obj_list = initialize_job_vacancy(vacancies)
    filtered_vacancies = filter_vacancies(vacancies_obj_list, filter_words, salary_range)
    sorted_vacancies = sorted(filtered_vacancies, reverse=True)
    print_vacancies(sorted_vacancies[:top_count])

    return vacancies


def remove_html_tags(text: str) -> str:
    """
    Удаляет HTML теги из заданной строки.

    :param text: Строка, из которой необходимо удалить HTML теги.
    :return: Строка с удаленными HTML тегами.
    """

    clean_text = re.sub('<.*?>', '', text)

    return clean_text


def initialize_job_vacancy(vacancies_list: list) -> list:
    """
    Инициализирует список объектов вакансий на основе данных из списка словарей.

    Для каждого словаря в входном списке создается объект класса JobVacancy, атрибуты которого заполняются
    соответствующими данными из словаря. При этом из описания вакансии удаляются HTML теги.

    :param vacancies_list: Список словарей, каждый из которых содержит информацию о вакансии.
    :return: Список объектов вакансий с заполненными атрибутами.
    """

    vacancies_obj_list = []

    for vacancy in vacancies_list:
        vacancies_obj_list.append(JobVacancy(vacancy['title'], vacancy['url'], vacancy['salary_min'],
                                             vacancy['salary_max'], remove_html_tags(vacancy['description'])))

    return vacancies_obj_list


def filter_vacancies(vacancies_list: list, filter_words: list, salary_range: str) -> list:
    """
    Фильтрует список вакансий по ключевым словам и диапазону заработной платы.

    Возвращает список вакансий, в названии, описании или любом другом текстовом поле которых содержится хотя бы одно
    из ключевых слов, указанных в filter_words, и чья заработная плата находится в заданном диапазоне salary_range.

    :param vacancies_list: Список объектов вакансий для фильтрации.
    :param filter_words: Список ключевых слов для фильтрации вакансий. Вакансия должна соответствовать хотя бы одному
                         слову из этого списка.
    :param salary_range: Диапазон заработной платы в форме строки из двух элементов - минимальной и максимальной
                         заработной платы. Вакансия должна предлагать заработную плату в этом диапазоне.
    :return: Список объектов вакансий, соответствующих указанным критериям фильтрации.
    """

    filtered_obj_list = []

    for vacancy in vacancies_list:
        if filter_words == vacancy and vacancy.comparison_salary(salary_range):
            filtered_obj_list.append(vacancy)

    return filtered_obj_list


def get_top_vacancies(vacancies_list: list, top_count: int) -> list:
    """
    Возвращает первые N вакансий из списка вакансий.

    Эта функция предназначена для извлечения указанного количества вакансий, начиная с начала списка. В случае,
    если количество запрашиваемых вакансий превышает количество вакансий в списке, будут возвращены все доступные
    вакансии.

    :param vacancies_list: Список вакансий, из которого будут извлекаться данные.
    :param top_count: Количество вакансий, которое необходимо извлечь из начала списка.
    :return: Список из первых N вакансий, где N - значение параметра top_count.
    """

    result = []

    for index in range(top_count):
        result.append(vacancies_list[index])

    return result


def print_vacancies(vacancies_list: list) -> None:
    """
    Выводит на экран список вакансий.

    Функция перебирает переданный список вакансий и выводит каждую вакансию на новой строке с порядковым номером.
    После каждой вакансии добавляется пустая строка для лучшей читаемости.

    :param vacancies_list: Список вакансий для вывода. Каждый элемент списка - это строчное представление вакансии.
    :return: None
    """

    print()

    for index, item in enumerate(vacancies_list):
        print(f"{index + 1}: {item}\n")
