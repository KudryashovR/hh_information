# hh_information
# Скрипт для работы с вакансиями

Этот скрипт предоставляет инструменты для поиска, фильтрации и сохранения вакансий в различных форматах. Весь процесс работы со скриптом состоит из нескольких основных этапов, которые описаны ниже.

## Поиск вакансий

Пользователю предложено ввести поисковый запрос для определения интересующих вакансий. Также необходимо указать количество вакансий для отображения в топе и ключевые слова для фильтрации. Последним шагом будет ввод диапазона зарплаты, чтобы ограничить поиски вакансий с желаемым доходом.

## Фильтрация вакансий

После того, как пользователь ввел все необходимые данные для поиска, скрипт выполняет поиск вакансий, инициализирует объекты JobVacancy, фильтрует полученный список вакансий по заданным критериям и выводит топ N вакансий, где N - это количество вакансий, указанное пользователем.

## Сохранение вакансий

Пользователю предлагается выбрать формат файла для сохранения результатов. Доступны следующие форматы:
1. JSON
2. CSV
3. TXT
4. Excel

После выбора формата необходимо ввести имя файла, в который будут сохранены результаты поиска. Файл автоматически сохранится в папку data.

### Процесс сохранения

1. JSON: Вакансии сохраняются в формате JSON.
2. CSV: Вакансии сохраняются в формате CSV.
3. TXT: Все вакансии сохраняются в текстовом файле. Список вакансий записывается как единый текст.
4. Excel: Вакансии сохраняются в виде таблицы в файле Excel.

## Ограничения

При вводе пользователем номера формата файла для сохранения допустимы только значения в диапазоне от 1 до 4. В случае ввода значения за пределами этого диапазона будет выведено сообщение: "Диапазон ввода 1-4". 

Для успешной работы скрипта необходимо наличие всех зависимостей и соответствующего окружения, а также доступа к API для поиска вакансий.