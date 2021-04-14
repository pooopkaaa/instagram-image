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


def main():
    images_folder = 'images/'
    Path(images_folder).mkdir(exist_ok=True)

    image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    image_title = 'hubble.jpeg'
    
    try:
        image_filepath = download_image(image_url, image_title, images_folder)
        print(image_filepath)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
