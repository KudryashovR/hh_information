import pytest

from src.classes import JobVacancy


def test_job_vacancy_init():
    """
    Тест на корректную инициализацию объекта класса JobVacancy. Проверяет, что все переданные атрибуты корректно
    сохраняются в объекте.
    """

    vacancy = JobVacancy("Python Developer", "http://example.com", 100000, 150000,
                         "Описание вакансии")

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary_min == 100000
    assert vacancy.salary_max == 150000
    assert vacancy.description == "Описание вакансии"


def test_validate_salary_with_none():
    """
    Тест проверяет метод валидации зарплаты (_validate_salary). При значении None для минимальной и максимальной
    зарплаты, должен устанавливаться 0.
    """

    vacancy = JobVacancy("Python Developer", "http://example.com")

    assert vacancy.salary_min == 0
    assert vacancy.salary_max == 0


def test_vacancies_equality():
    """
    Тест проверяет правильность работы метода __eq__. Две вакансии считаются равными, если их минимальные зарплаты
    равны.
    """

    vacancy1 = JobVacancy("Python Developer", "http://example1.com", 100000, 150000)
    vacancy2 = JobVacancy("Frontend Developer", "http://example2.com", 100000, 120000)

    assert vacancy1 == vacancy2


def test_vacancies_inequality():
    """
    Тест проверяет, что объекты вакансий с разными минимальными зарплатами не равны.
    """

    vacancy1 = JobVacancy("Python Developer", "http://example1.com", 100000, 150000)
    vacancy2 = JobVacancy("Frontend Developer", "http://example2.com", 90000, 120000)

    assert vacancy1 != vacancy2


def test_vacancies_less_than():
    """
    Тест проверяет правильность работы метода __lt__. Один объект вакансии считается меньше другого, если его
    минимальная зарплата меньше.
    """

    vacancy1 = JobVacancy("Python Developer", "http://example1.com", 90000, 150000)
    vacancy2 = JobVacancy("Frontend Developer", "http://example2.com", 100000, 120000)

    assert vacancy1 < vacancy2


def test_vacancies_repr():
    """
    Тест проверяет форматированный вывод информации о вакансии с помощью метода __repr__. Включает в себя проверку
    формата строки с названием, зарплатой, URL и описание вакансии.
    """
    vacancy = JobVacancy("Python Developer", "http://example.com", 100000, None,
                         "Используйте Python для разработки.")
    expected_repr = ("Python Developer (Зарплата: от 100000 и выше), http://example.com\nОписание: Используйте Python "
                     "для разработки.")

    assert repr(vacancy) == expected_repr
