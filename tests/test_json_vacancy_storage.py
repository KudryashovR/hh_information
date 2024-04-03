import json
import pytest
import os
from tempfile import NamedTemporaryFile


from src.classes import JSONVacancyStorage


@pytest.fixture
def temp_file():
    """
    Создает временный файл.
    """

    with NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as f:
        yield f.name

    os.unlink(f.name)


@pytest.fixture
def storage_with_vacancy(temp_file):
    """
    Создает хранилище с одной вакансией.
    """

    storage = JSONVacancyStorage(filename=temp_file)
    storage.add_vacancy({'title': 'Developer', 'company': 'DevCompany'})

    return storage


def test_add_vacancy(temp_file):
    """
    Проверяет добавление вакансии.
    """

    storage = JSONVacancyStorage(filename=temp_file)
    vacancy = {'title': 'QA Engineer', 'company': 'Test Inc'}
    storage.add_vacancy(vacancy)

    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]['title'] == 'QA Engineer'
    assert data[0]['company'] == 'Test Inc'


def test_get_vacancies(storage_with_vacancy):
    """
    Проверяет получение вакансий по критериям.
    """

    vacancies = storage_with_vacancy.get_vacancies({'title': 'Developer'})

    assert len(vacancies) == 1
    assert vacancies[0]['title'] == 'Developer'
    assert vacancies[0]['company'] == 'DevCompany'


def test_delete_vacancies(storage_with_vacancy, temp_file):
    """
    Проверяет удаление вакансий по критерию.
    """

    storage_with_vacancy.delete_vacancies({'title': 'Developer'})

    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 0
