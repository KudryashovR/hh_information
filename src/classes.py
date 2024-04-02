import requests


from src.abstract_classes import VacancyService


class HHVacancyService(VacancyService):
    """
    Сервис для работы с вакансиями с сайта hh.ru.

    Позволяет выполнять поиск вакансий с помощью API hh.ru по определённым критериям поиска.
    Возвращает информацию о вакансиях, такую как название, URL, информация о зарплате и описание.
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса HHVacancyService.

        Устанавливает базовый URL для доступа к API вакансий hh.ru.
        """

        self.base_url = "https://api.hh.ru/vacancies"

    def fetch_vacancies(self, search_query: str) -> list:
        """
        Выполняет запрос к API hh.ru для получения вакансий по заданному поисковому запросу.

        :param search_query: текст поискового запроса, по которому необходимо найти вакансии.
        :return: список словарей, каждый из которых содержит информацию о вакансии (название, URL, информация о зарплате
                 и описание).
        """

        params = {"text": search_query, "area": "113"} # 113 - Регион поиска - Россия
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        return self._parse_vacancies(data['items'])

    @staticmethod
    def _parse_vacancies(vacancies_data: list) -> list:
        """
        Парсит список вакансий, полученный от API, преобразуя его в удобный для работы формат.

        :param vacancies_data: список словарей с данными вакансий, полученный от API.
        :return: список вакансий, где каждая вакансия представлена в виде словаря с ключами: title, url, salary_min,
                 salary_max, description.
        """

        vacancies = []

        for v in vacancies_data:
            title = v.get('name', 'Название не указаноэ')
            url = v.get('alternate_url', 'URL не указан')
            salary_info = v.get('salary', {})

            if salary_info:
                salary_min = salary_info.get('from', 'Не указано')
                salary_max = salary_info.get('to', 'Не указано')
            else:
                salary_min, salary_max = 'Не указано', 'Не указано'

            description = v.get('snippet', {}).get('requirement', 'Описание отсутствует')

            if not description:
                description = 'Описание отсутствует'

            vacancies.append({"title": title, "url": url, "salary_min": salary_min, "salary_max": salary_max,
                              "description": description})

        return vacancies
