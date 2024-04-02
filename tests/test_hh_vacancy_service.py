import pytest


from src.classes import HHVacancyService


@pytest.fixture
def service():
    return HHVacancyService()


def test_parse_vacancies_normal_data(service):
    """
    Тестирует корректность разбора входных данных, когда все поля присутствуют.
    """

    input_data = [{"name": "Senior Python Developer", "alternate_url": "https://example.com/vacancy/1",
                   "salary": {"from": 200_000, "to": 300_000}, "snippet": {"requirement": "Опыт работы с Python"},}]
    expected_output = [{"title": "Senior Python Developer", "url": "https://example.com/vacancy/1",
                        "salary_min": 200000, "salary_max": 300000, "description": "Опыт работы с Python"}]

    assert service._parse_vacancies(input_data) == expected_output


def test_parse_vacancies_missing_fields(service):
    """
    Тестирует поведение парсера при отсутствии некоторых полей во входных данных.
    """

    input_data = [{"name": "Junior Python Developer", "salary": None, "snippet": {"requirement": ""}}]
    expected_output = [{"title": "Junior Python Developer", "url": "URL не указан", "salary_min": "Не указано",
                        "salary_max": "Не указано", "description": "Описание отсутствует"}]

    assert service._parse_vacancies(input_data) == expected_output


def test_parse_vacancies_empty_list(service):
    """
    Тестирует обработку пустого списка вакансий.
    """

    input_data = []
    expected_output = []

    assert service._parse_vacancies(input_data) == expected_output
