from abc import ABC, abstractmethod


class VacancyService(ABC):
    """
    Абстрактный класс для работы с API платформы hh.ru
    """

    @abstractmethod
    def fetch_vacancies(self, search_query):
        pass


class VacancyStorage(ABC):
    """
    Абстрактный класс для сохранения/открытия/удаления файлов с вакансиями.
    """

    @abstractmethod
    def add_vacancy(self, vacancy_data):
        pass

    @abstractmethod
    def get_vacancies(self, search_criteria):
        pass

    @abstractmethod
    def delete_vacancies(self, search_criteria):
        pass
