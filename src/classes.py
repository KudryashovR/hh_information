import requests
from typing import Union
import json
import csv
import pandas as pd

from src.abstract_classes import VacancyService, VacancyStorage


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

        Константные значения:
            - area: 113 - Регион поиска - Россия
            - per_page: - Количество возвращаемых вакансий

        :param search_query: текст поискового запроса, по которому необходимо найти вакансии.
        :return: список словарей, каждый из которых содержит информацию о вакансии (название, URL, информация о зарплате
                 и описание).
        """

        params = {"text": search_query, "area": "113", "per_page": 100}
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

    def __eq__(self, other: list) -> bool:
        """
        Определяет наличие ключевых слов в описании вакансии.

        :param other: Ключевые слова.
        :return: True, если ключевое слово входит в описание, иначе False.
        """

        for key in other:
            if key in self.description:
                return True

        return False

    def __lt__(self, other: 'JobVacancy') -> bool:
        """
        Определяет, меньше ли минимальная зарплата текущей вакансии, чем у другой.

        :param other: Вакансия для сравнения.
        :return: True, если минимальная зарплата текущей вакансии меньше, иначе False.
        """

        self_salary_min = self.salary_min if type(self.salary_min) is int else 0
        other_salary_min = other.salary_min if type(other.salary_min) is int else 0

        return self_salary_min < other_salary_min

    def __le__(self, other: str) -> bool:
        """
        Определяет, меньше или равна ли максимальная зарплата текущей вакансии, чем у другой.

        :param other: Цена для сравнения.
        :return: True, если максимальная зарплата текущей вакансии меньше или равна, иначе False.
        """

        if self.salary_max is not int:
            return True

        return self.salary_max <= int(other)

    def __ge__(self, other: str) -> bool:
        """
        Определяет, больше или равна ли минимальная зарплата текущей вакансии, чем у другой.

        :param other: Цена для сравнения.
        :return: True, если минимальная зарплата текущей вакансии больше или равна, иначе False.
        """

        if self.salary_min is not int:
            return True

        return self.salary_min >= int(other)

    def comparison_salary(self, other: str) -> bool:
        """
        Определяет, входит ли вакансия в заданный диапазон цен.

        :param other: Заданный диапазон цен.
        :return: True, если зарплата текущей вакансии в заданном диапазоне, иначе False.
        """

        min_salary, max_salary = other.split(' - ')

        return min_salary <= self <= max_salary

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

        return f"{self.title} ({salary}), {self.url}\nОписание: {self.description}"


class JSONVacancyStorage(VacancyStorage):
    """
    Класс для хранения информации о вакансиях в формате JSON.

    Этот класс поддерживает добавление, поиск и удаление вакансий в хранилище, представленном JSON-файлом.

    Атрибуты:
        - filename (str): Путь к файлу JSON, используемому для хранения данных о вакансиях.

    Методы:
        - add_vacancy(vacancy_data): Добавляет новую вакансию в хранилище.
        - get_vacancies(search_criteria): Возвращает список вакансий, соответствующих заданным критериям поиска.
        - delete_vacancies(search_criteria): Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализирует экземпляр класса JSONVacancyStorage.

        :param filename: Путь к JSON-файлу для хранения данных о вакансиях.
        """

        self.filename = filename

    def add_vacancy(self, vacancy_data: dict) -> None:
        """
        Добавляет новую вакансию в хранилище.

        :param vacancy_data: Словарь с данными о вакансии для добавления.
        """

        try:
            data = self._load_data()
        except FileNotFoundError:
            data = []
        except json.decoder.JSONDecodeError:
            data = []

        data.append(vacancy_data)
        self._save_data(data)

    def get_vacancies(self, search_criteria: dict) -> list:
        """
        Возвращает список вакансий, соответствующих заданным критериям поиска.

        :param search_criteria: Словарь с критериями для поиска вакансий.
        :return: Список вакансий (в формате словарей), соответствующих критериям поиска.
        """

        data = self._load_data()
        result = [vacancy for vacancy in data if all(vacancy.get(key) == value for key, value in
                                                     search_criteria.items())]

        return result

    def delete_vacancies(self, search_criteria: dict) -> None:
        """
        Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.

        :param search_criteria: Словарь с критериями для поиска и удаления вакансий.
        """

        data = self._load_data()
        data = [vacancy for vacancy in data if not all(vacancy.get(key) == value for key, value in
                                                       search_criteria.items())]
        self._save_data(data)

    def _load_data(self) -> list:
        """
        Загружает данные из json файла.

        :return: Список вакансий, сохраненных в файлах (в формате словарей).
        """

        with open(self.filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _save_data(self, data: list) -> None:
        """
        Сохраняет данные в json файл.

        :param data: Список вакансий (в формате словарей) для сохранения.
        """

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class CSVVacancyStorage(VacancyStorage):
    """
    Класс для хранения информации о вакансиях в формате CSV.

    Этот класс поддерживает добавление, поиск и удаление вакансий в хранилище, представленном JSON-файлом.

    Атрибуты:
        - filename (str): Путь к файлу CSV, используемому для хранения данных о вакансиях.

    Методы:
        - add_vacancy(vacancy_data): Добавляет новую вакансию в хранилище.
        - get_vacancies(search_criteria): Возвращает список вакансий, соответствующих заданным критериям поиска.
        - delete_vacancies(search_criteria): Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализирует экземпляр класса CSvVacancyStorage.

        :param filename: Путь к CSV-файлу для хранения данных о вакансиях.
        """

        self.filename = filename

    def add_vacancy(self, vacancy_data: dict) -> None:
        """
        Добавляет новую вакансию в хранилище.

        :param vacancy_data: Словарь с данными о вакансии для добавления.
        """

        try:
            data = self._load_data()
        except FileNotFoundError:
            data = []
        except json.decoder.JSONDecodeError:
            data = []

        data.append(vacancy_data)
        self._save_data(data)

    def get_vacancies(self, search_criteria: dict) -> list:
        """
        Возвращает список вакансий, соответствующих заданным критериям поиска.

        :param search_criteria: Словарь с критериями для поиска вакансий.
        :return: Список вакансий (в формате словарей), соответствующих критериям поиска.
        """

        data = self._load_data()
        result = [vacancy for vacancy in data if all(vacancy.get(key) == value for key, value in
                                                     search_criteria.items())]

        return result

    def delete_vacancies(self, search_criteria: dict) -> None:
        """
        Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.

        :param search_criteria: Словарь с критериями для поиска и удаления вакансий.
        """

        data = self._load_data()
        data = [vacancy for vacancy in data if not all(vacancy.get(key) == value for key, value in
                                                       search_criteria.items())]
        self._save_data(data)

    def _load_data(self) -> list:
        """
        Загружает данные из csv файла.

        :return: Список вакансий, сохраненных в файлах (в формате словарей).
        """

        with open(self.filename, newline='', encoding='utf-8') as csvfile:
            return list(csv.DictReader(csvfile))

    def _save_data(self, data: list) -> None:
        """
        Сохраняет данные в csv файл.

        :param data: Список вакансий (в формате словарей) для сохранения.
        """

        keys = data[0].keys() if data else []

        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


class TXTVacancyStorage(VacancyStorage):
    """
    Класс для хранения информации о вакансиях в формате TXT.

    Этот класс поддерживает добавление, поиск и удаление вакансий в хранилище, представленном JSON-файлом.

    Атрибуты:
        - filename (str): Путь к файлу TXT, используемому для хранения данных о вакансиях.

    Методы:
        - add_vacancy(vacancy_data): Добавляет новую вакансию в хранилище.
        - get_vacancies(search_criteria): Возвращает список вакансий, соответствующих заданным критериям поиска.
        - delete_vacancies(search_criteria): Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализирует экземпляр класса JSONVacancyStorage.

        :param filename: Путь к JSON-файлу для хранения данных о вакансиях.
        """

        self.filename = filename

    def add_vacancy(self, vacancy_data: list) -> None:
        """
        Добавляет новую вакансию в хранилище.

        :param vacancy_data: Список с данными о вакансии для добавления.
        """

        try:
            data = self._load_data()
        except FileNotFoundError:
            data = []
        except json.decoder.JSONDecodeError:
            data = []

        data.append(vacancy_data)
        self._save_data(data)

    def get_vacancies(self, search_criteria: dict) -> list:
        """
        Возвращает список вакансий, соответствующих заданным критериям поиска.

        :param search_criteria: Словарь с критериями для поиска вакансий.
        :return: Список вакансий (в формате словарей), соответствующих критериям поиска.
        """

        data = self._load_data()
        result = [vacancy for vacancy in data if all(vacancy.get(key) == value for key, value in
                                                     search_criteria.items())]

        return result

    def delete_vacancies(self, search_criteria: dict) -> None:
        """
        Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.

        :param search_criteria: Словарь с критериями для поиска и удаления вакансий.
        """

        data = self._load_data()
        data = [vacancy for vacancy in data if not all(vacancy.get(key) == value for key, value in
                                                       search_criteria.items())]
        self._save_data(data)

    def _load_data(self) -> list:
        """
        Загружает данные из txt файла.

        :return: Список вакансий, сохраненных в файлах (в формате словарей).
        """

        with open(self.filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readline()]

    def _save_data(self, data: list) -> None:
        """
        Сохраняет данные в txt файл.

        :param data: Список вакансий (в формате словарей) для сохранения.
        """

        with open(self.filename, 'w', encoding='utf-8') as file:
            for vacancy in data:
                file.write(str(vacancy) + '\n')


class XLSXVacancyStorage(VacancyStorage):
    """
    Класс для хранения информации о вакансиях в формате JSON.

    Этот класс поддерживает добавление, поиск и удаление вакансий в хранилище, представленном JSON-файлом.

    Атрибуты:
        - filename (str): Путь к файлу JSON, используемому для хранения данных о вакансиях.

    Методы:
        - add_vacancy(vacancy_data): Добавляет новую вакансию в хранилище.
        - get_vacancies(search_criteria): Возвращает список вакансий, соответствующих заданным критериям поиска.
        - delete_vacancies(search_criteria): Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализирует экземпляр класса JSONVacancyStorage.

        :param filename: Путь к JSON-файлу для хранения данных о вакансиях.
        """

        self.filename = filename

    def add_vacancy(self, vacancy_data: list) -> None:
        """
        Добавляет новую вакансию в хранилище.

        :param vacancy_data: Список с данными о вакансии для добавления.
        """

        try:
            data = self._load_data()
        except FileNotFoundError:
            data = []
        except json.decoder.JSONDecodeError:
            data = []

        data.append(vacancy_data)
        self._save_data(data)

    def get_vacancies(self, search_criteria: dict) -> list:
        """
        Возвращает список вакансий, соответствующих заданным критериям поиска.

        :param search_criteria: Словарь с критериями для поиска вакансий.
        :return: Список вакансий (в формате словарей), соответствующих критериям поиска.
        """

        data = self._load_data()
        result = [vacancy for vacancy in data if all(vacancy.get(key) == value for key, value in
                                                     search_criteria.items())]

        return result

    def delete_vacancies(self, search_criteria: dict) -> None:
        """
        Удаляет вакансии, соответствующие заданным критериям поиска, из хранилища.

        :param search_criteria: Словарь с критериями для поиска и удаления вакансий.
        """

        data = self._load_data()
        data = [vacancy for vacancy in data if not all(vacancy.get(key) == value for key, value in
                                                       search_criteria.items())]
        self._save_data(data)

    def _load_data(self) -> list:
        """
        Загружает данные из xlsx файла.

        :return: Список вакансий, сохраненных в файлах (в формате словарей).
        """

        data_frame = pd.read_excel(self.filename)

        return data_frame.to_dict('records')

    def _save_data(self, data: list) -> None:
        """
        Сохраняет данные в xlsx файл.

        :param data: Список вакансий (в формате словарей) для сохранения.
        """

        data_frame = pd.DataFrame(data)
        data_frame.to_excel(self.filename, index=False)
