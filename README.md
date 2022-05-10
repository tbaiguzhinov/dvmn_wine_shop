# Новое русское вино

Сайт магазина авторского вина "Новое русское вино".

## Запуск

- Скачайте код
- Установите зависимости
`pip install -r requirements.txt`
- Запустите сайт командой
`python3 main.py wine.xlsx`
- Перейдите на сайт по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

Если Вы положите файл в папку проекта, вместо адреса файла можно указать только его название.

## Формат исходных данных

Код использует Excel файл в формате .xlsx в нижеуказанном виде:

| Категория | Название | Сорт | Цена | Картинка | Акция |
| --------- | -------- | ---- | ---- | -------- | ----- |
| Вино      | Вкуснота | Саперави | 10 руб. | wine.png | Выгода |

Пример файла также загружен в репозиторий - "wine.xlsx".
