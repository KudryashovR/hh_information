import src.utils as utils


def main():
    founded_vacancies = utils.get_vacancies()

    user_answer = input("Выберите формат файла для сохранения:\n"
                        "1. JSON\n"
                        "2. CSV\n"
                        "3. TXT\n"
                        "4. Excel\n")

    match user_answer:
        case '1' | '2' | '3' | '4':
            utils.save_vacancies(founded_vacancies, user_answer)
        case _:
            print("Диапазон ввода [1-4]")


if __name__ == '__main__':
    main()
