# Космический Инстаграм

Скрипты для автоматической загрузки, редактировании и публикации изображений, связанных с космической тематикой.

- Загрузка изображений с телескопа [Hubble](https://ru.wikipedia.org/wiki/%D0%A5%D0%B0%D0%B1%D0%B1%D0%BB_(%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF)) с помощью предоставленного [API](http://hubblesite.org/api/documentation).
- Загрузка изображений с последних запусков [SpaceX](https://ru.wikipedia.org/wiki/SpaceX) с помощью предоставленного [API](https://documenter.getpostman.com/view/2025350/RWaEzAiG#bc65ba60-decf-4289-bb04-4ca9df01b9c1).
- Редактирование и публикация изображений в личный аккаунт [Instagram](https://www.instagram.com/).

## Установка

- Для работы скрипта у вас должен быть установлен [Python3](https://www.python.org/downloads/) (не ниже версии 3.6.0).
- Скачайте код.
- Рекомендуется использовать [virtualenv/env](https://docs.python.org/3/library/venv.html) для изоляции проекта.
- Установите зависимости для работы скрипта:

```bash
pip install -r requirements.txt
```
- Создайте файл `.env`, который содержит `INSTAGRAM_LOGIN` и `INSTAGRAM_PASSWORD` доступа к личному аккаунту [Instagram](https://www.instagram.com/).

```
INSTAGRAM_LOGIN=
INSTAGRAM_PASSWORD=
```

## Настройка запуска

- Для загрузки изображений с телескопа [Hubble](https://ru.wikipedia.org/wiki/%D0%A5%D0%B0%D0%B1%D0%B1%D0%BB_(%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF)) необходимо запустить скрипт `fetch_hubble.py` с переданными параметрами:

Параметр | Пример 1 | Пример 2 | Описание 
-------- | -------- | -------- | ------
`--folder`<br>`-f` | `--folder my-images/`| `-f my-images/` | В какую папку загружить изображения.<br>По умолчанию `images/`.
`--collection`<br>`-c`| `--collection holiday_cards` | `-c holiday_cards` | Какую коллекцию изображений загрузить.
`--id`<br>`-i`| `--id 1` | `-i 1` | Какой id изображения загрузить.

- Для загрузки изображений с последних запусков [SpaceX](https://ru.wikipedia.org/wiki/SpaceX) необходимо запустить скрипт `fetch_spacex.py` с переданным параметром:

Параметр | Пример 1 | Пример 2 | Описание 
-------- | -------- | -------- | ------
`--folder`<br>`-f` | `--folder my-images/`| `-f my-images/` | В какую папку загружить изображения. По умолчанию<br>`images/`.

- Для редактирования и публикации изображений в личный аккаунт [Instagram](https://www.instagram.com/) необходимо запустить скрипт `upload_images.py` с переданными обязательными параметрами:

Параметр | Пример 1 | Пример 2 | Описание 
-------- | -------- | -------- | ------
`--folder`<br>`-f` | `--folder my-images/`| `-f my-images/` | В какой папке находятся загруженные изображения.
`--modify`<br>`-m`| `--modify modify_images/` | `-c modify_images/` | В какой папке будут находиться<br>отредактированные и опубликованные<br>изображения.


## Запуск

- Пример запуска скрипта `fetch_hubble.py`:
```bash
python fetch_hubble.py -f my-images/ --collection holiday_cards -i 1
```

- Пример запуска скрипта `fetch_spacex.py`:
```bash
python fetch_spacex.py -f my-images/
```

- Пример запуска скрипта `upload_images.py`:
```bash
python upload_images.py -f my-images/ -m modify_images/
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).