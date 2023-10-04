
import requests
import json
from requests import Response

"""код, который будет сохранять всех персонажей (имена), которые снимались в фильмах с Дарт Вейдером, в тестовый файл"""

"""проверка кода осуществляется через pytest:
python -m pytest -s -v"""


class Test_http_methods:
    headers = {'Content-type': 'application/json'}
    cookie = ""

    @staticmethod
    def get(url):
        result = requests.get(url, headers=Test_http_methods.headers, cookies=Test_http_methods.cookie) # получение данных get-запроса по переданному url
        assert result.status_code == 200, "Метод get вернул невалидный статус, дальнейшая проверка невозможна"
        return result

    @staticmethod
    def get_param_list(response: Response, value, param=None): #получение списка параметров
        get_params = json.loads(response.text)
        if param: # если параметр передан в методе, то проверяется, есть ли такое значение параметра в полученном ответе
            assert param in get_params.values(), f"'{param}' не существует в параметрах ответа"
            print(f'{param} существует в параметрах. Продолжение проверки данных')
        list_params = get_params[value]
        return list_params #возвращение списка параметров из ответа

    @staticmethod
    def get_heroes_data(list_params, param): # получение данных о героях
        hero_links, hero_names = [], []
        assert list_params is not None
        for film in list_params:
            res = Test_http_methods()
            response = res.get(film)
            data = res.get_param_list(response, param) # получение  списка или строки параметров
            if isinstance(data, list):
                for link in data:
                    if link not in hero_links:
                        hero_links.append(link)

            elif isinstance(data, str):
                if 'Darth Vader' not in data:
                    hero_names.append(data)
        if hero_links:
            return res.get_heroes_data(hero_links, "name") # отправка списка ссылок на героев с целью получения имен этим же методом
        print("Имена героев, которые снимались с Дартом Вейдером: ", hero_names)
        with open('characters_names.txt', mode='w+', encoding='utf-8') as file:
            print("\n".join(hero_names), file=file)
        print("Тестирование завершено успешно/ Проверьте созданный файл characters_names.txt с именами героев")

dart = Test_http_methods()
get_res = dart.get('https://swapi.dev/api/people/4/')
lst = dart.get_param_list(get_res,  'films', 'Darth Vader')
dart.get_heroes_data(lst, "characters")

# @staticmethod
# def get_heroes_links(list_films): # получение списка  героев по списку фильмов
#     hero_links = []
#     hero_names = []
#     for film in list_films:
#         res = Test_http_methods()
#         response = res.get(film)
#         links = res.get_param_list(response, "characters")
#         for link in links:
#             if link not in hero_links:
#                 hero_links.append(link)
#
#     for hero_link in list(hero_links):
#         res = Test_http_methods()
#         response = res.get(hero_link)
#         character = res.get_param_list(response, "name")
#         if 'Darth Vader' not in character:
#             hero_names.append(character)
#     print(hero_names)
#     with open('characters_names.txt', mode='w+', encoding='UTF-8') as file:
#         print("\n".join(hero_names), file=file)
#     return hero_links