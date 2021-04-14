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


def main():
    images_folder = 'images/'
    Path(images_folder).mkdir(exist_ok=True)

    api_url = 'https://api.spacexdata.com/v4/launches/latest'

    try:
        image_links = fetch_image_links_spacex_last_launch(api_url)
        for image_id, image_link in enumerate(image_links, start=1):
            image_title = f'spacex{image_id}.jpg'
            image_filepath = download_image(image_link, image_title, images_folder)
            print(image_filepath)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
