import os
import requests
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ['TOKEN']


def get_user(token: str) -> str:
    url = 'https://api-ssl.bitly.com/v4/user'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def shorten_link(token: str, link: str) -> str:
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': link
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    short_url = response.json()['link']
    return short_url


def count_clicks(token: str, link: str) -> str:

    link = link.replace('https://', '').replace('http://', '')
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token: str, url: str) -> bool:
    url = url.replace('https://', '').replace('http://', '')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    link = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    response = requests.get(link, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return False
    return True


def main() -> None:
    user_input = input('Введите ссылку: ')
    if is_bitlink(TOKEN, user_input):
        print("Вы ввели битлинк. Количество переходов по нему: ", count_clicks(TOKEN, user_input))
    else:
        try:
            print("Битлинк по вашей ссылке: ", shorten_link(TOKEN, user_input))
        except requests.exceptions.HTTPError:
            print("Введённая строка не является ни битлинком, ни длинной ссылкой. "
                  "Попробуйте ещё раз, перезапустив программу")


if __name__ == '__main__':
    main()
