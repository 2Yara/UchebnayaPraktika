# Notes API
Notes API — это учебный REST-сервис для управления заметками, созданный на Flask.   

## Цель проекта
Цель проекта — освоить разработку backend-API, работу с HTTP, JSON, базами данных, тестирование и деплой.  

## Локальный запуск
Для локального запуска клонируйте репозиторий: `git clone https://github.com/<твой_логин>/notes_api.git`, перейдите в папку: `cd notes_api`, создайте виртуальное окружение: `python -m venv venv`, активируйте его: `venv\Scripts\activate` (Windows) или `source venv/bin/activate` (Linux/macOS), установите зависимости: `pip install -r requirements.txt`, запустите приложение: `python app.py` или `flask run`.  

## Деплой на Render
Для деплоя на Render создайте аккаунт, подключите GitHub-репозиторий, выберите Web Service, укажите Build Command: `pip install -r requirements.txt`, Start Command: `gunicorn app:app`, и после сборки получите публичный URL.     

## Примеры API-запросов
Примеры API-запросов: получить все заметки — `curl http://127.0.0.1:5000/notes`;    
Создать заметку — `curl -X POST http://127.0.0.1:5000/notes -H "Content-Type: application/json" -d '{"title":"Купить хлеб","content":"Не забыть молоко"}'`;     
Получить одну заметку — `curl http://127.0.0.1:5000/notes/1`;   
Обновить заметку — `curl -X PUT http://127.0.0.1:5000/notes/1 -H "Content-Type: application/json" -d '{"title":"Купить хлеб и молоко"}'`;   
Удалить заметку — `curl -X DELETE http://127.0.0.1:5000/notes/1`.  

## Тестирование
Для тестирования установите pytest: `pip install pytest`, создайте файл `test_app.py` с тестами для эндпоинтов и запустите `pytest` в корне проекта.    

## Демо
Живое демо доступно по ссылке: `<URL_от_Render>`.

## Автор 
Попова Т. С. - garfielb_2Yara