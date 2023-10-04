"""Методы для проверки ответов наших запросов"""
import json
from requests import Response


class Checking():

    """метод проверки статус кода"""
    @staticmethod
    def check_status(response: Response, status_code):
        if response.status_code == status_code:
            print("Успешно!!!! Статус код = " + str(response.status_code))
        else:
            print("Статус кода не совпадает")

    """метод для проверки наличия полей"""
    @staticmethod
    def check_json_token(response: Response, expected_value):
        token = json.loads(response.text)
        assert list(token) == expected_value
        print("Все поля присутствуют")

    """метод для проверки значений обязательных полей"""
    @staticmethod
    def check_json_value(response: Response, field_name, expected_value):
        check = response.json()
        check_info = check.get(field_name)
        assert check_info == expected_value
        print(f'{field_name} верен')

    @staticmethod
    def check_json_search_word_in_value(response: Response, field_name, search_word):
        check = response.json()
        check_info = check.get(field_name)
        if search_word in check_info:
            print(f'Слово {field_name} найдено в значении')
        else:
            print("Ожидаемое слово не найдено")