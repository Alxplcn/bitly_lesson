import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


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
    parsed_link = urlparse(link)
    link = f'{parsed_link.netloc}{parsed_link.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token: str, url: str) -> bool:
    parsed_url = urlparse(url)
    url = f'{parsed_url.netloc}{parsed_url.path}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    link = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    response = requests.get(link, headers=headers)
    return response.ok


def main() -> None:
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    user_input = input('Введите ссылку: ')
    try:
        if is_bitlink(token, user_input):
            print("Вы ввели битлинк. Количество переходов по нему: ", count_clicks(token, user_input))
        else:
            print("Битлинк по вашей ссылке: ", shorten_link(token, user_input))
    except requests.exceptions.HTTPError:
        print("Введённая строка не является ни битлинком, ни длинной ссылкой. "
              "Попробуйте ещё раз, перезапустив программу")


if __name__ == '__main__':
    main()
