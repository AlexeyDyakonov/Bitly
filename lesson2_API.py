import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse
import os

def shorten_link(token, link):
    headers = {"Authorization": token}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json={"long_url": link}
    )
    response.raise_for_status()
    total_bitlink = response.json()['link']
    return total_bitlink


def count_clicks(token, link):
    parsed_url = urlparse(link)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    headers = {"Authorization": token}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=headers,
        params={"units": '-1'}
    )
    response.raise_for_status()
    number_of_clicks = response.json()['total_clicks']
    return number_of_clicks


def is_bitlink(token, link):
    parsed_url = urlparse(link)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    headers = {"Authorization": token}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}',
        headers=headers
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Создает битлинк или считает количество кликов по битлинку')
    parser.add_argument('url', help='Ссылка на сайт или битлинк')
    args = parser.parse_args()
    user_input = args.url
    try:
        if is_bitlink(token, user_input):
            print("Сумма кликов равна {0}\
                ".format(str(count_clicks(token, user_input))))
        else:
            print("Битлинк введеной ссылки {0}\
                ".format(str(shorten_link(token, user_input))))
    except requests.exceptions.HTTPError:
        print('Cсылка введена неправильно')