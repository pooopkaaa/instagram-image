import os
from os import listdir
from pathlib import Path
import requests
from PIL import Image
from instabot import Bot
from dotenv import load_dotenv


def modify_images(downloaded_images_folder, modify_images_folder):
    for filename in listdir(downloaded_images_folder):
        image = Image.open(Path(downloaded_images_folder).joinpath(filename))
        converted_image = image.convert('RGB')
        if converted_image.width//converted_image.height >= 1:
            converted_image.thumbnail((1080, 1080))
            converted_image.save(
                    Path(modify_images_folder)
                    .joinpath(filename).with_suffix('.jpg'),
                    format="JPEG")
        else:
            converted_image.thumbnail((converted_image.width, 1080))
            coordinates = [-(1080-converted_image.width)//2,
                           0,
                           converted_image.width+(1080-converted_image.width)//2,
                           1080]
            cropped_image = converted_image.crop(coordinates)
            cropped_image.save(
                    Path(modify_images_folder)
                    .joinpath(filename).with_suffix('.jpg'),
                    format="JPEG")
    print('Изображения -> подготовлены к загрузке')


def upload_images_to_instagram(folder):
    load_dotenv()
    bot = Bot()
    bot.login(username=os.environ['LOGIN'], password=os.environ['PASSWORD'])
    for filename in listdir(folder):
        filepath = Path(folder).joinpath(filename)
        bot.upload_photo(filepath)
    print('Изображения -> опубликованы')


def main():
    downloaded_images_folder = 'images'
    modify_images_folder = 'modify_images'
    Path(modify_images_folder).mkdir(exist_ok=True)

    try:
        modify_images(downloaded_images_folder, modify_images_folder)
        upload_images_to_instagram(modify_images_folder)
    except requests.exceptions.HTTPError as request_error:
        exit(f'Не могу получить ответ от сервера -> {request_error}')


if __name__ == '__main__':
    main()
