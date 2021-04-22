import os
from urllib.parse import urlsplit, unquote
import requests


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
    unquote_url = unquote(url)
    url_path = urlsplit(unquote_url).path
    filename = os.path.split(url_path)[-1]
    file_extension = os.path.splitext(filename)[-1]
    return file_extension


if __name__ == '__main__':
    pass
