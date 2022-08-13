import time
import json

import requests



# Рассчет рейтинга между А и В
def calc_elo(is_a, rate_a, rate_b, times):
    """
    :param is_a: Победил ли А
    :param rate_a: Рейтинг А
    :param rate_b: Рейтинг В
    :param times: Кол-во голосов
    :return: Новый рейтинг
    """
    # Ожидаемое
    E = 1 / (1 + 10 * ((rate_b - rate_a) / 400))
    if E > 2100:
        k = 10
    elif times > 30:
        k = 15
    else:
        k = 30
    return rate_a + k * (is_a - E)


class Parser:
    def __init__(self):
        self.__API = "https://api.vk.com/method/"
        self.__access_token = self._token()

    def _token(self):
        with open('auth.json', 'r') as auth_file:
            return json.load(auth_file)["access_token"]

    # Парсер поиска по универу(1000)
    def search_university(self, uni_id, uni_year, fields, sex):
        try:
            search = requests.get(self.__API + "users.search", params={
                "access_token": self.__access_token,
                "university": uni_id,
                "sex": sex,
                "count": 1000,
                "university_year": uni_year,
                "fields": fields,
                "v": 5.131,
            })
            data = search.json()["response"]["items"]
            print(data)
        except Exception as e:
            print("[ERROR] You so hot. Wait 2 sec, dude")
            time.sleep(2)

        return data
