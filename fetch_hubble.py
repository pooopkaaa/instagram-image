import os
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import argparse
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_command_line_args():
    parser = argparse.ArgumentParser(description='Загрузка изображений опубликованных\
                                     с телескопа Hubble с помощью предоставленного API.\
                                     Укажите коллекция изображений, которое необходимо скачать.\
                                     Дополнительно можно загрузить изображение по заданному id.')
    parser.add_argument('-f',
                        '--folder',
                        default='images/',
                        help='Укажите в какую папку загрузить изображения.')
    parser.add_argument('-c',
                        '--collection',
                        help='Укажите какую коллекцию изображений загрузить.')
    parser.add_argument('-i',
                        '--id',
                        help='Укажите какой id изображения загрузить.')
    return parser.parse_args()


def get_response(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response


def download_image(url, filename, folder):
    response = get_response(url)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_file_extension_from_url(url):
    return os.path.splitext(os.path.split(urlsplit(unquote(url)).path)[-1])[-1]


def fetch_hubble_from_collection(collection_name, folder):
    url = f'http://hubblesite.org/api/v3/images/{collection_name}'
    response = get_response(url)
    image_ids = [image_element['id'] for image_element in response.json()]
    for image_id in image_ids:
        fetch_hubble_from_id(image_id, folder)


def fetch_hubble_from_id(image_id, folder):
    image_url = urljoin('https://',
                        get_response(f'http://hubblesite.org/api/v3/image/{image_id}')
                        .json()['image_files'][-1]['file_url'])
    image_title = f'hubble{image_id}{get_file_extension_from_url(image_url)}'
    download_image(image_url, image_title, folder)


def main():
    command_line_args = get_command_line_args()
    images_folder = command_line_args.folder
    Path(images_folder).mkdir(exist_ok=True)
    hubble_collection_name = command_line_args.collection
    hubble_image_id = command_line_args.id

    try:
        if hubble_collection_name:
            fetch_hubble_from_collection(hubble_collection_name, images_folder)
        if hubble_image_id:
            fetch_hubble_from_id(hubble_image_id, images_folder)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
