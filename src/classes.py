import requests
from typing import Union

from src.abstract_classes import VacancyService


class HHVacancyService(VacancyService):
    """
    Сервис для работы с вакансиями с сайта hh.ru.

    Позволяет выполнять поиск вакансий с помощью API hh.ru по определённым критериям поиска. Возвращает информацию
    о вакансиях, такую как название, URL, информация о зарплате и описание.
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

        params = {"text": search_query, "area": "113"}  # 113 - Регион поиска - Россия
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


class JobVacancy:
    """
    Класс для представления информации о вакансии.

    Объект класса содержит информацию о названии вакансии, URL, зарплате и описании. Поддерживает сравнение вакансий
    по минимальной зарплате и форматированный вывод информации о вакансии.
    """

    def __init__(self, title: str, url: str, salary_min: int = None, salary_max: int = None,
                 description: str = '') -> None:
        """
        Инициализирует новый экземпляр класса JobVacancy.

        :param title: Название вакансии.
        :param url: URL вакансии.
        :param salary_min: Минимальная зарплата (если не указана, предполагается 0).
        :param salary_max: Максимальная зарплата (если не указана, предполагается None).
        :param description: Описание вакансии (по умолчанию пустая строка).
        """

        self.title = title
        self.url = url
        self.salary_min = self._validate_salary(salary_min)
        self.salary_max = self._validate_salary(salary_max)
        self.description = description

    @staticmethod
    def _validate_salary(salary: Union[int, None]) -> int:
        """
        Проверяет и корректирует значение зарплаты.

        :param salary: Значение зарплаты для проверки.
        :return: Переданное значение, если оно не None, иначе 0.
        """

        return salary if salary is not None else 0

    def __eq__(self, other: 'JobVacancy') -> bool:
        """
        Определяет равенство вакансий по минимальной зарплате.

        :param other: Вакансия для сравнения.
        :return: True, если минимальные зарплаты равны, иначе False.
        """

        return self.salary_min == other.salary_min

    def __lt__(self, other: 'JobVacancy') -> bool:
        """
        Определяет, меньше ли минимальная зарплата текущей вакансии, чем у другой.

        :param other: Вакансия для сравнения.
        :return: True, если минимальная зарплата текущей вакансии меньше, иначе False.
        """

        return self.salary_min < other.salary_min

    def __repr__(self) -> str:
        """
        Возвращает строковое представление вакансии.

        Включает название вакансии, информацию о зарплате, URL и краткое описание.
        :return: Строковое представление вакансии.
        """

        salary = f"Зарплата: от {self.salary_min}"

        if self.salary_max:
            salary += f" до {self.salary_max}"
        else:
            salary += " и выше"

        descr = self.description[:60] + '...' if len(self.description) > 60 else self.description

        return f"{self.title} ({salary}), {self.url}\nОписание: {descr}"
