from abc import ABC, abstractmethod


class VacancyService(ABC):
    """
    Абстрактный класс для работы с API платформы hh.ru
    """

    @abstractmethod
    def fetch_vacancies(self, search_query):
        pass
