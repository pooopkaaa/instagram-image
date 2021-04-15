import os
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import requests
import urllib3
from PIL import Image
from os import listdir
from os import walk


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
IMAGES_SPACEX_FOLDER = os.path.join('images', 'spacex')
IMAGES_HUBBLE_FOLDER = os.path.join('images', 'hubble')
IMAGES_RESIZE_FOLDER = os.path.join('images', 'resize')


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


def fetch_spacex_last_launch(url):
    Path(IMAGES_SPACEX_FOLDER).mkdir(exist_ok=True, parents=True)
    response = get_response(url)
    image_urls = response.json()['links']['flickr']['original']
    for image_id, image_url in enumerate(image_urls, start=1):
        image_title = f'spacex{image_id}{get_file_extension_from_url(image_url)}'
        download_image(image_url, image_title, IMAGES_SPACEX_FOLDER)


def fetch_hubble_from_collection(url):
    Path(IMAGES_HUBBLE_FOLDER).mkdir(exist_ok=True, parents=True)
    response = get_response(url)
    image_ids = [image_element['id'] for image_element in response.json()]
    for image_id in image_ids:
        image_url = urljoin(
                'https://',
                get_response(f'http://hubblesite.org/api/v3/image/{image_id}').json()
                ['image_files'][-1]['file_url'])
        image_title = f'{image_id}{get_file_extension_from_url(image_url)}'
        download_image(image_url, image_title, IMAGES_HUBBLE_FOLDER)


def modify_image(folder):
    for filepath in listdir(folder)
    Path(IMAGES_RESIZE_FOLDER).mkdir(exist_ok=True, parents=True)
    image = Image.open(filepath)
    image.thumbnail((1080, 1080))
    conver_image = image.convert('RGB')
    conver_image.save(os.path.join(IMAGES_RESIZE_FOLDER, '1.jpg'), format="JPEG")


def main():
    hubble_collection_name = 'holiday_cards'
    api_spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    api_hubble_url = f'http://hubblesite.org/api/v3/images/{hubble_collection_name}'
    filepath = 'images/spacex/spacex1.jpg'
    
    try:
        # fetch_spacex_last_launch(api_spacex_url)
        # fetch_hubble_from_collection(api_hubble_url)
        modify_image(IMAGES_SPACEX_FOLDER)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
