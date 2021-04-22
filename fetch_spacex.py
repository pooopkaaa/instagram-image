from pathlib import Path
import argparse
import requests
import urllib3
from handler import get_response, download_image, get_file_extension_from_url


def get_command_line_args():
    parser = argparse.ArgumentParser(description='Загрузка изображений\
                                     опубликованных с последнего запуска\
                                     SpaceX с помощью предоставленного API.')
    parser.add_argument('-f',
                        '--folder',
                        default='images/',
                        help='Укажите в какую папку загрузить изображения.')
    return parser.parse_args()


def fetch_spacex_last_launch(folder):
    url = 'https://api.spacexdata.com/v4/launches/latest'
    response = get_response(url)
    image_urls = response.json()['links']['flickr']['original']
    for image_id, image_url in enumerate(image_urls, start=1):
        image_title = f'spacex{image_id}{get_file_extension_from_url(image_url)}'
        download_image(image_url, image_title, folder)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    command_line_args = get_command_line_args()
    images_folder = command_line_args.folder
    Path(images_folder).mkdir(exist_ok=True)

    try:
        fetch_spacex_last_launch(images_folder)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
