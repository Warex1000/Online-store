# shop

import django

print(django.get_version())
print('hello world')

'''
python3 manage.py makemigrations - Django использует миграции для переноса изменений в моделях 
(добавление поля, удаление модели и т.д.) на структуру базы данных.
python3 manage.py migrate
pip3 install pillow - install for using models.ImageField fore pictures

What me do:

- register App 'mainapp' in sittings in INSTALLED_APPS
- create models
- make: makemigrations and migrate
- register models in admin


# 2:24:45