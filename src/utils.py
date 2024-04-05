import re


from src.classes import JobVacancy


def remove_html_tags(text):
    """

    :param text:
    :return:
    """

    clean_text = re.sub('<.*?>', '', text)

    return clean_text


def initialize_job_vacancy(vacancies_list):
    """

    :param vacancies_list:
    :return:
    """

    vacancies_obj_list = []

    for vacancy in vacancies_list:
        vacancies_obj_list.append(JobVacancy(vacancy['title'], vacancy['url'], vacancy['salary_min'],
                                             vacancy['salary_max'], remove_html_tags(vacancy['description'])))

    return vacancies_obj_list


def filter_vacancies(vacancies_list, filter_words, salary_range):
    """

    :param vacancies_list:
    :param filter_words:
    :param salary_range:
    :return:
    """

    filtered_obj_list = []

    for vacancy in vacancies_list:
        if filter_words == vacancy and vacancy.comparison_salary(salary_range):
            filtered_obj_list.append(vacancy)

    return filtered_obj_list


def get_top_vacancies(vacancies_list, top_count):
    """

    :param vacancies_list:
    :param top_count:
    :return:
    """

    result = []

    for index in range(top_count):
        result.append(vacancies_list[index])

    return result


def print_vacancies(vacancies_list):
    """

    :param vacancies_list:
    :return:
    """

    print()

    for index, item in enumerate(vacancies_list):
        print(f"{index + 1}: {item}\n")
