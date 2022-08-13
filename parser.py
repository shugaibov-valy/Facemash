import json  # Для работы с json файлами
import time  # sleep
from components.users.models import User
import requests  # http запросы

# Подхватываем токен из json файла
with open('auth_data.json', 'r') as auth_file:
    auth_data = json.load(auth_file)

access_token = auth_data['access_token']
API = 'https://api.vk.com/method/'  # Обращение к методу API
API_VERSION = 5.131


# Подписчики в паблике(определить смещение для сбора информации). Подробнее: https://vk.com/dev/groups.getMembers
def get_member_count(group_id):
    try:  # Блок, для того чтоб перехватывать ошибки запроса
        count = requests.get(f'{API}groups.getMembers', params={  # Обращение к API с параметрами
            'access_token': access_token,  # Ключ доступа
            'group_id': group_id,
            'offset': 0,  # Смещение(грубо первые 1000 с минимальным id)
            'v': API_VERSION
        }).json()['response']['count']
    except Exception as e:  # Если произошла ошибка
        print(f'[LOG] {e}')  # Вывод ошибки
        time.sleep(1)
        get_member_count(group_id)  # Повторяем зарос(рекурсия)
    else:  # Если ответ удачный, возвращаем кол-во подписчиков
        return count


# Информация о пидписчиках паблика со всеми доп. полями. Подробнее: https://vk.com/dev/groups.getMembers
def get_members_data(group_id):
    members_data = []
    offset, max_offset = 0, get_member_count(group_id) // 1000 + 1  # Определяем максимальное смещение
    while offset < max_offset + 1:
        try:
            data = requests.get(f'{API}groups.getMembers', params={
                'access_token': access_token,  # Ключ доступа
                'group_id': group_id,
                'offset': offset * 1000,  # API позволяет получить инфрмацию о 1000 за 1 зарос поэтому юзаем смещения
                'fields': 'sex, bdate, city, country, photo_max_orig, '  # Получаем всю возможную инфу о пользователе
                          'online, online_mobile, lists, domain, has_mobile, '  # Чтоб потом не писать
                          'contacts, connections, site, education, universities, '  # лишних запросов
                          'schools, can_post, can_see_all_posts, can_see_audio, '  # Но это временно, я считаю да-да
                          'can_write_private_message, status, last_seen, '  # Позднее реализую через execute(!)
                          'common_count, relation, relatives',
                'v': API_VERSION
            }).json()['response']['items']
        except Exception as e:  # Если произошла ошибка
            print(f'[LOG] {e}')  # Вывод ошибки
            time.sleep(1)
        else:
            offset += 1
            for item in data:
                if item["sex"] == 1:
                    User.create_new_user(item["id"], str(item["photo_max_orig"]))
                    members_data.append([item["id"], item["photo_max_orig"]])
    # Визуально понять, как выглядит ответ, который нужно распарсить
    data = {'Processed': members_data}  # делаем словарь
    data = json.dumps(data)  # словарь в json строку
    data = json.loads(data)  # json строка в словари
    write_to_file('data.json', data)  # Появится файл data.json посмотреть его notepad++ с плагином json viewer
    # https://ibb.co/L8bVCsT Скрин с json viewer чтоб имет абстрактное пердставление и понимать как парсить
    print('Success')


# Файловый поток в json
def read_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


# Запись json в файл одной строкой
def write_to_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


def main():
    get_members_data('loveregion152')


if __name__ == '__main__':
    main()

