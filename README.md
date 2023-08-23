# TelephoneDirectory
## Телефонная книга с консольным интерфейсом

###1. task_json.py

Данная программа может обработать json-коллекци данных в виде телефонного справочника
Каждая запись содержить ФИО, организацию, личный и рабочий номера телфонов

Создание нового файла возможно с помощью модуля Faker, который автоматически генерирует тестовые данные

##2. task_txt.py

Более тривиальная версия телефонного справочника, которая обрабатывает файлы в формате .txt
Данные сохраняются в строки и считываются построчно, соответственно.

Также есть возможность создания файла с тестовыми данными с помощью модуля Faker

##3. book1.txt book2.json

Данные текстовые файлы представляют собой тестовые данные, сгенерированные в программах
Есть одно замечание по сгенерированным данным: иногда в ФИО нарушается порядок следования аргументов, но, в целом, это не создает затруднений для тестирования проекта

## Для тестирования достаточно запустить одну из программ