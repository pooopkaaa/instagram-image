import os
from pathlib import Path
import requests


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def download_image(url, filename, folder):
    response = get_response(url)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def fetch_image_links_spacex_last_launch(url):
    response = get_response(url)
    return response.json()['links']['flickr']['original']


def fetch_image_links_hubble(url):
    response = get_response(url)
    return [image_file['file_url'] for image_file in response.json()['image_files']]


def main():
    images_folder = 'images/'
    Path(images_folder).mkdir(exist_ok=True)

    api_spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    api_hubble_url = 'http://hubblesite.org/api/v3/image/1/'
    try:
        # image_spacex_links = fetch_image_links_spacex_last_launch(api_spacex_url)
        # for image_id, image_link in enumerate(image_spacex_links, start=1):
        #     image_title = f'spacex{image_id}.jpg'
        #     image_filepath = download_image(image_link, image_title, images_folder)
        #     print(image_filepath)
        image_hubble_links = fetch_image_links_hubble(api_hubble_url)
        print(image_hubble_links)

    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
