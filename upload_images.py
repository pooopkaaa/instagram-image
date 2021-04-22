import os
from os import listdir
from pathlib import Path
import argparse
import requests
from PIL import Image
from instabot import Bot
from dotenv import load_dotenv


def get_command_line_args():
    parser = argparse.ArgumentParser(description='Редактирую изображения по определенным условиям.\
                                     Публикую изображений в ваш instagram аккаунт.')
    parser.add_argument('-f',
                        '--folder',
                        required=True,
                        help='Укажите папку в которой хранятся загруженные изображения.')
    parser.add_argument('-m',
                        '--modify',
                        required=True,
                        help='Укажите папку в которой будут хранится опубликованные изображения.')
    return parser.parse_args()


def modify_images(downloaded_images_folder, modify_images_folder):
    for filename in listdir(downloaded_images_folder):
        image = Image.open(Path(downloaded_images_folder).joinpath(filename))
        converted_image = image.convert('RGB')
        if converted_image.width//converted_image.height >= 1:
            converted_image.thumbnail((1080, 1080))
            converted_image.save(Path(modify_images_folder)
                                 .joinpath(filename).with_suffix('.jpg'),
                                 format='JPEG')
        else:
            converted_image.thumbnail((converted_image.width, 1080))
            coordinates = [-(1080-converted_image.width)//2,
                           0,
                           converted_image.width+(1080-converted_image.width)//2,
                           1080]
            cropped_image = converted_image.crop(coordinates)
            cropped_image.save(Path(modify_images_folder)
                               .joinpath(filename).with_suffix('.jpg'),
                               format='JPEG')


def upload_images_to_instagram(instagram_login, instagram_password, folder):
    bot = Bot()
    bot.login(username=instagram_login, password=instagram_password)
    for filename in listdir(folder):
        filepath = Path(folder).joinpath(filename)
        bot.upload_photo(filepath)


def main():
    load_dotenv()
    instagram_login = os.environ['INSTAGRAM_LOGIN']
    instagram_password = os.environ['INSTAGRAM_PASSWORD']
    command_line_args = get_command_line_args()
    downloaded_images_folder = command_line_args.folder
    modify_images_folder = command_line_args.modify
    Path(modify_images_folder).mkdir(exist_ok=True)

    modify_images(downloaded_images_folder, modify_images_folder)
    upload_images_to_instagram(instagram_login, instagram_password, modify_images_folder)


if __name__ == '__main__':
    main()
