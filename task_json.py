from faker import Faker
from random import choice
import os.path
import json
from time import sleep

class TelephoneBook:

	def creating_new_file(self, file_name: str, length: int):
		"""Создает новый файл из тестовых данных в json формате
		file_name - имя для нового файла без формата
		length - количество записей, которые создадутся рандомно с помощью модуля Faker
		"""
		self.telephone_directory = DataFactory(file_name, length).telephone_directory
		self.length = len(self.telephone_directory)
		self.file_name = file_name+'.json'
		self.length_pages()

	def open_existing_file(self, file_name: str):
		"""Открывает существующий файл в json формате в текущей директории
		file_name - имя существующего файйла без формата
		"""
		file_name += '.json'
		if os.path.exists(file_name):
			with open(file_name, 'r', encoding='utf-8') as file:
				self.telephone_directory = json.load(file)
				self.length = len(self.telephone_directory)
				self.file_name = file_name
				self.length_pages()
				return self.telephone_directory
		else:
			return None

	def contents(self):
		"""Выводит оглавление телефонной книги"""
		print('-----------------Оглавление------------------------')
		letters = {}
		for person in enumerate(self.telephone_directory, 1):
			letter = person[1]['last_name'][0]
			num_of_page = (person[0]-1)//10+1
			letters[letter] = letters.get(letter, num_of_page)
		for letter, number in letters.items():
			print(f'{letter}------------------------------------{number}')
	
	def open_page(self, page_num=1):
		"""Открывает страницу телефонного справочника
		page_num - номер страницы, которую необходимо открыть
		"""
		if page_num <= 0 or page_num > self.pages:
			print('Такой страницы не существует')
			print(f'Страниц в телефонном справочнике: {self.pages}')
		else:
			self.opened_page = page_num
			return self.show_page()

	def show_page(self):
		"""Возвращает список записей открытой страницы"""
		if self.opened_page*10+1 >= self.length:
			return self.telephone_directory[(self.opened_page-1)*10:]
		else:
			return self.telephone_directory[(self.opened_page-1)*10:self.opened_page*10]

	def show_person(self, person: dict):
		"""Возвращает строчное отображение записи из справочника
		person - запись из справочника
		"""
		return f"{person['last_name']},{person['first_name']}, {person['middle_name']}, {person['organization']}, {person['personal_phone']}, {person['work_phone']}"

	def next_page(self):
		"""Возвращает следующую страницу справочника, если она есть,
		None - если следующей странцы нет"""
		if self.opened_page+1 > self.pages:
			return None
		else:
			self.opened_page += 1
			return self.show_page()

	def previous_page(self):
		"""Возвращает предыдущую страницу справочника, если она есть,
		None - если предыдущей странцы нет"""
		if self.opened_page-1 < 1:
			return None
		else:
			self.opened_page -= 1
			return self.show_page()

	def actual_page(self):
		"""Возвращает строку с номер открытой страницы"""
		return f'Открыта страница номер {self.opened_page}'
		
	def length_pages(self):
		"""Вызывается при открытии, создании и изменении справочника"""
		if self.length%10 == 0:
			self.pages = self.length//10
		else:
			self.pages = self.length//10 + 1

	def search_person(self, person_dict: dict):
		"""Производит поиск записи или записей по произвольному количеству параметров
		person_dict - словарь с параметрами поиска
		"""
		# first_name, middle_name, last_name
		# organization, personal_phone, work_phone
		result = []
		for person in enumerate(self.telephone_directory, 1):
			if person in result:
				continue
			else:
				for key, value in person_dict.items():
					if person[1].get(key, None) == value:
						result.append(person)
		return result

	def edit_person(self, person: dict, person_dict: dict):
		"""Производит изменение в записи по произвольному количеству параметров
		person - запись из спавочника
		person_dict - словарь с параметрами для изменения
		"""
		id_person = self.telephone_directory.index(person)
		# first_name, middle_name, last_name
		# organization, personal_phone, work_phone
		edit_person = self.telephone_directory.pop(id_person)
		for key, value in person_dict.items():
			if value == '':
				continue
			elif key in person_dict.keys():
				edit_person[key] = value
		self.telephone_directory.append(edit_person)
		self.write_changes()

	def delete_person(self, person: dict):
		"""Производит удаление в записи из справочника
		person - запись из спавочника
		"""
		id_person  = self.telephone_directory.index(person)
		# first_name, middle_name, last_name
		# organization, personal_phone, work_phone
		self.telephone_directory.pop(id_person)
		self.write_changes()

	def write_changes(self):
		"""Записывает изменение после редактирования, добавления или удаления записи"""
		temp = []
		for person in self.telephone_directory:
			if person not in temp:
				temp.append(person)
		self.telephone_directory = temp
		with open(self.file_name, 'w', encoding='utf-8') as tel:
			json.dump(sorted(self.telephone_directory, key=lambda x: x['last_name']), tel, ensure_ascii=False)
		self.length = len(self.telephone_directory)
		self.length_pages()

	def add_person(self, last_name, first_name, middle_name, organization, personal_phone, work_phone):
		"""Добавляет запись в справочник
		Принимает все параметры записи
		"""
		# first_name, middle_name, last_name
		# organization, personal_phone, work_phone
		person = {
				'first_name': first_name,
				'middle_name': middle_name,
				'last_name': last_name,
				'organization': organization,
				'personal_phone': personal_phone,
				'work_phone': work_phone,
				 }
		self.telephone_directory.append(person)
		self.write_changes()



class DataFactory: # Создает тестовые данные с помощью модуля Faker

	def __init__(self, file_name: str, length=30):
		"""Принимает имя файла и количество записей"""
		self.length = length
		self.fake = Faker('ru_RU')
		self.file_name = file_name + '.json'
		self.creating_file()

	def creating_file(self):
		"""Создает файл и заполняет его тестовыми данными"""
		self.create_phones()
		self.create_companies()
		self.create_people()

		telephone_directory = []
		for name, tel1, tel2 in zip(self.people, self.personal_phones, self.work_phones):
			person = {
				'first_name': name[0],
				'middle_name': name[1],
				'last_name': name[2],
				'organization': choice(self.companies),
				'personal_phone': tel1,
				'work_phone': tel2,
				 }
			telephone_directory.append(person)
		self.telephone_directory = telephone_directory

		with open(self.file_name, 'w', encoding='utf-8') as tel:
			json.dump(sorted(self.telephone_directory, key=lambda x: x['last_name']), tel, ensure_ascii=False)

	def create_phones(self):
		"""Создает телефонные номера по указанному шаблону"""
		phones = ['+7'+self.fake.numerify('(###)###-##-##') for _ in range(self.length*2)]
		self.personal_phones = phones[:self.length]
		self.work_phones = phones[self.length:]

	def create_companies(self):
		"""Создает названия организаций"""
		self.companies = [self.fake.company() for _ in range(self.length//3+1)]

	def create_people(self):
		"""Создает ФИО людей"""
		self.people = [self.fake.name().split() for _ in range(self.length)]


class DirectoryInterface:

	def __init___(self):
		self.main_menu()

	def main_menu(self):

		options = {
		'1': self.create_file,
		'2': self.open_file,
		}

		choices = [
			'1. Создать новый файл телефонного справочника\n',
			'2. Открыть существующий файл телефонного справочника\n'
			'3. Введите любой другой символ, чтобы завершить работу\n']
		choice = input(''.join(choices))

		if choice not in options.keys():
			print('Закрытие программы через:')
			print('3')
			sleep(1)
			print('2')
			sleep(1)
			print('1')
			sleep(1)
		else:
			options[choice]()

	def create_file(self):
		file_name = input('\nВведите имя для нового файла:\n')
		length = int(input('\nВведите длину нового файла:\n'))
		self.directory = TelephoneBook()
		self.directory.creating_new_file(file_name, length)
		print(f'\nФайл {file_name} успешно создан\n')
		self.file_options()

	def open_file(self):
		file_name = input('\nВведите имя существующего файла без расширения:\n')
		self.directory = TelephoneBook()
		self.directory.open_existing_file(file_name)
		if not self.directory.telephone_directory:
			print('\nТакого файла не существует\n')
			self.main_menu()
		else:
			print(f'\nФайл {file_name} открыт\n')
			self.file_options()

	def file_options(self):
		options = {
		'1': self.contents,
		'2': self.open_page,
		'3': self.search_person,
		'4': self.add_person,
		'5': self.edit_person,
		'6': self.delete_person,
		'7': self.main_menu,
		}
		choices = [
			'1. Открыть оглавление\n',
			'2. Открыть страницу справочника\n',
			'3. Поиск записей\n',
			'4. Добавление записи\n',
			'5. Изменение записи\n',
			'6. Удаление записи\n',
			'7. Вернуться в менеджер файлов\n',
			]
		choice = input(''.join(choices))
		options[choice]()

	def contents(self):
		self.directory.contents()
		self.file_options()

	def open_page(self):
		page_num = int(input('\nВведите номер страницы:\n'))
		page = self.directory.open_page(page_num)
		print(f'---------СТРАНИЦА_НОМЕР_{page_num}------------')
		for person in page:
			print(self.directory.show_person(person))
		self.page_menu()

	def page_menu(self):

		options = {
		'1': self.open_page,
		'2': self.next_page,
		'3': self.previous_page,
		'4': self.file_options
		}

		choices = [
			'1. Открыть страницу по номеру\n',
			'2. Открыть следующую страницу\n',
			'3. Открыть предыдущую страницу\n',
			'4. Вернуться в главное меню\n',
			]

		choice = input(''.join(choices))
		options[choice]()

	def next_page(self):
		page = self.directory.next_page()
		if not page:
			print('Это последняя страница')
			self.page_menu()
		else:
			page_num = self.directory.opened_page
			print(f'---------СТРАНИЦА_НОМЕР_{page_num}------------')
			for person in page:
				print(self.directory.show_person(person))
			self.page_menu()

	def previous_page(self):
		page = self.directory.previous_page()
		if not page:
			print('Это первая страница')
			self.page_menu()
		else:
			page_num = self.directory.opened_page
			print(f'---------СТРАНИЦА_НОМЕР_{page_num}------------')
			for person in page:
				print(self.directory.show_person(person))
			self.page_menu()

	def add_person(self):
		last_name = input('Введите фамилию нового пользователя:\n')
		firs_name = input('Введите имя нового пользователя:\n')
		middle_name = input('Введите отчество нового пользователя:\n')
		organization = input('Введите организацию нового пользователя:\n')
		personal_phone = input('Введите личный номер телефона нового пользователя:\n')
		work_phone = input('Введите рабочий номер телефона нового пользователя:\n')
		self.directory.add_person(last_name, firs_name, middle_name, organization, personal_phone, work_phone)
		print('\nЗапись успешно создана\n')
		self.file_options()

	def search_person(self):
		print('\nВведите параметры, по которым нужно найти запись')
		print('Достаточно ввести один параметр, остальные можно пропустить\n')
		last_name = input('Введите фамилию пользователя:\n')
		first_name = input('Введите имя пользователя:\n')
		middle_name = input('Введите отчество пользователя:\n')
		organization = input('Введите организацию пользователя:\n')
		personal_phone = input('Введите личный номер телефона пользователя:\n')
		work_phone = input('Введите рабочий номер телефона пользователя:\n')
		person_dict = {
				'first_name': first_name,
				'middle_name': middle_name,
				'last_name': last_name,
				'organization': organization,
				'personal_phone': personal_phone,
				'work_phone': work_phone,
				 }
		person = self.directory.search_person(person_dict)

		if len(person) == 0:
			print("\nНе удалось найти запись\n")
			self.file_options()
		elif len(person) == 1:
			print(f'\n{self.directory.show_person(person[0][1])}\n')
		else:
			for num, data in person:
				print(f'{num} {self.directory.show_person(data)}\n')
			num = int(input('Введите номер подходящей записи:\n'))
			if num not in [i[0] for i in person]:
				print('Такого номера среди найденных записей нет')
			else:
				print(f'\n{self.directory.show_person(self.directory.telephone_directory[num-1])}\n')
		self.file_options()

	def edit_person(self):
		print('Введите параметры, по которым нужно найти запись для редактирования')
		print('Достаточно ввести один параметр, остальные можно пропустить\n')
		last_name = input('Введите фамилию пользователя:\n')
		first_name = input('Введите имя пользователя:\n')
		middle_name = input('Введите отчество пользователя:\n')
		organization = input('Введите организацию пользователя:\n')
		personal_phone = input('Введите личный номер телефона пользователя:\n')
		work_phone = input('Введите рабочий номер телефона пользователя:\n')
		person_dict = {
				'first_name': first_name,
				'middle_name': middle_name,
				'last_name': last_name,
				'organization': organization,
				'personal_phone': personal_phone,
				'work_phone': work_phone,
				 }
		person = self.directory.search_person(person_dict)
		if len(person) == 0:
			print("\nНе удалось найти запись\n")
			self.file_options()
		elif len(person) == 1:
			person = person[0][1]
			print(f'\n{self.directory.show_person(person)}\n')
		else:
			for num, data in person:
				print(f'{num} {self.directory.show_person(data)}\n')
			num = int(input('Введите номер подходящей записи:\n'))
			if num not in [i[0] for i in person]:
				print('Такого номера среди найденных записей нет')
			else:
				person = self.directory.telephone_directory[num-1]
				print(f'\n{self.directory.show_person(person)}\n')

		print('Введите параметры, которые нужно изменить')
		print('Можно ввести только те параметры, которые нужно изменить\n')
		last_name = input('Введите фамилию пользователя:\n')
		first_name = input('Введите имя пользователя:\n')
		middle_name = input('Введите отчество пользователя:\n')
		organization = input('Введите организацию пользователя:\n')
		personal_phone = input('Введите личный номер телефона пользователя:\n')
		work_phone = input('Введите рабочий номер телефона пользователя:\n')

		edit_dict = {
				'first_name': first_name,
				'middle_name': middle_name,
				'last_name': last_name,
				'organization': organization,
				'personal_phone': personal_phone,
				'work_phone': work_phone,
				 }
		self.directory.edit_person(person, edit_dict)
		print('\nЗапись успешно изменена\n')
		self.file_options()

	def delete_person(self):

		print('Введите параметры, по которым нужно найти запись для удаления')
		print('Достаточно ввести один параметр, остальные можно пропустить\n')
		last_name = input('Введите фамилию пользователя:\n')
		first_name = input('Введите имя пользователя:\n')
		middle_name = input('Введите отчество пользователя:\n')
		organization = input('Введите организацию пользователя:\n')
		personal_phone = input('Введите личный номер телефона пользователя:\n')
		work_phone = input('Введите рабочий номер телефона пользователя:\n')
		person_dict = {
				'first_name': first_name,
				'middle_name': middle_name,
				'last_name': last_name,
				'organization': organization,
				'personal_phone': personal_phone,
				'work_phone': work_phone,
				 }

		person = self.directory.search_person(person_dict)
		if len(person) == 0:
			print("\nНе удалось найти запись\n")
			self.file_options()
		elif len(person) == 1:
			person = person[0][1]
			print(f'\n{self.directory.show_person(person)}\n')
		else:
			for num, data in person:
				print(f'{num} {self.directory.show_person(data)}\n')
			num = int(input('Введите номер подходящей записи:\n'))
			if num not in [i[0] for i in person]:
				print('\nТакого номера среди найденных записей нет\n')
				self.file_options()
			else:
				person = self.directory.telephone_directory[num-1]
				print(f'\n{self.directory.show_person(person)}\n')
		print('\nВы уверены, что хотите удалить дынную запись?\n')

		choices = [
			'1. Удалить пользователя\n',
			'2. Отмена\n',
			]

		choice = input(''.join(choices))

		if choice == '1':
			self.directory.delete_person(person)
			print('\nЗапись успешно удалена\n')
		else:
			print('\nУдаление записи отменено\n')

		self.file_options()



a = DirectoryInterface().main_menu()