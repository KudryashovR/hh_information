import re


from src.classes import JobVacancy


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
