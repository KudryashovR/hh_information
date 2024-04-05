from src.classes import HHVacancyService, JobVacancy
import src.utils as utils


def main():
    search_query = input("Введите поисковый запрос: ")
    top_count = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000 - 150000): ")

    hh_api = HHVacancyService()
    vacancies = hh_api.fetch_vacancies(search_query)
    vacancies_obj_list = utils.initialize_job_vacancy(vacancies)
    filtered_vacancies = utils.filter_vacancies(vacancies_obj_list, filter_words, salary_range)
    utils.print_vacancies(utils.get_top_vacancies(sorted(filtered_vacancies), top_count))


if __name__ == '__main__':
    main()
