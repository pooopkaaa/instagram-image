import os
from pathlib import Path
import requests
from urllib.parse import urlsplit, unquote, urljoin
import os


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


def get_image_title(url, image_hubble_id):
    return f'{image_hubble_id}{os.path.splitext(os.path.split(urlsplit(unquote(url)).path)[-1])[-1]}'


def fetch_image_links_spacex_last_launch(url):
    response = get_response(url)
    return response.json()['links']['flickr']['original']


def fetch_image_links_hubble(url):
    response = get_response(url)
    return [image_file['file_url'] for image_file in response.json()['image_files']]


def main():
    images_spacex_folder = os.path.join('images', 'spacex')
    images_hubble_folder = os.path.join('images', 'hubble')
    Path(images_spacex_folder).mkdir(exist_ok=True, parents=True)
    Path(images_hubble_folder).mkdir(exist_ok=True, parents=True)

    image_hubble_id = 1

    api_spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    api_hubble_url = f'http://hubblesite.org/api/v3/image/{image_hubble_id}/'
    try:
        # image_spacex_links = fetch_image_links_spacex_last_launch(api_spacex_url)
        # for image_id, image_link in enumerate(image_spacex_links, start=1):
        #     image_title = f'spacex{image_id}.jpg'
        #     image_filepath = download_image(image_link, image_title, images_folder)
        #     print(image_filepath)
        image_hubble_link = urljoin('https://', fetch_image_links_hubble(api_hubble_url)[-1])
        image_hubble_title = get_image_title(image_hubble_link, image_hubble_id)
        download_image(image_hubble_link, image_hubble_title, images_hubble_folder)

    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
