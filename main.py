import os
from os import listdir
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import requests
import urllib3
from PIL import Image


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def fetch_spacex_last_launch(folder):
    url = 'https://api.spacexdata.com/v4/launches/latest'
    response = get_response(url)
    image_urls = response.json()['links']['flickr']['original']
    for image_id, image_url in enumerate(image_urls, start=1):
        image_title = f'spacex{image_id}{get_file_extension_from_url(image_url)}'
        download_image(image_url, image_title, folder)


def fetch_hubble_from_collection(collection_name, folder):
    url = f'http://hubblesite.org/api/v3/images/{collection_name}'
    response = get_response(url)
    image_ids = [image_element['id'] for image_element in response.json()]
    for image_id in image_ids:
        fetch_hubble_from_id(image_id, folder)


def fetch_hubble_from_id(image_id, folder):
    image_url = urljoin(
            'https://',
            get_response(f'http://hubblesite.org/api/v3/image/{image_id}').json()
            ['image_files'][-1]['file_url'])
    image_title = f'hubble{image_id}{get_file_extension_from_url(image_url)}'
    download_image(image_url, image_title, folder)


def modify_images(folder):
    for filename in listdir(folder):
        filepath = os.path.join(folder, filename)
        image = Image.open(filepath)
        image.thumbnail((1080, 1080))
        print(image.mode)
        conver_image = image.convert('RGB')
        conver_image.save(filepath, format="JPEG")


def main():
    images_folder = 'images'
    Path(images_folder).mkdir(exist_ok=True)

    hubble_collection_name = 'holiday_cards'

    try:
        fetch_spacex_last_launch(images_folder)
        fetch_hubble_from_id('1', images_folder)
        fetch_hubble_from_collection(hubble_collection_name, images_folder)
        modify_images(images_folder)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
