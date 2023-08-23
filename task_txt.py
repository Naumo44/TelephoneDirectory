from faker import Faker
from random import choice
import os.path
from time import sleep

class TelephoneBook:

	def __init__(self):
		self.chosen_person = -1
		self.mode = None
		self.mods ={
			'change': self.change_person,
			'delete': self.delete_person
		}
		self.options = {
		'1': self.contents,
		'2': self.open_page,
		'3': self.search_person,
		'4': self.add_person,
		'5': self.change_person,
		'6': self.delete_person,
		'7': self.main_menu,

	}
		self.main_menu()

	def main_menu(self):
		choices = [
			'1. Создать новый файл телефонного справочника\n',
			'2. Открыть существующий файл телефонного справочника\n'
			'3. Введите любой другой символ, чтобы завершить работу\n']
		choice = input(''.join(choices))
		if choice == '1':
			self.creating_new_file()
		elif choice == '2':
			self.open_existing_file()
		else:
			print('Закрытие программы через:')
			print('3')
			sleep(1)
			print('2')
			sleep(1)
			print('1')
			sleep(1)




	def file_options(self):
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
		self.options[choice]()

	def creating_new_file(self):
		length = input('Введите количество записей в телефонном справочнике:\n')
		file_name = input('Введите название файла нового телефонного справочника:\n')
		self.telephone_directory = sorted(DataFactory(length=length, file_name=file_name).telephone_directory)
		self.length = len(self.telephone_directory)
		self.file_name = file_name+'.txt'
		self.length_pages()
		self.file_options()

	def open_existing_file(self):
		file_name = input('Введите название файла существующиего телефонного справочника:\n')+'.txt'
		if os.path.exists(file_name):
				with open(file_name, 'r', encoding='utf-8') as file:
					self.telephone_directory = [i.rstrip() for i in file.readlines()]
					self.length = len(self.telephone_directory)
					self.file_name = file_name
					self.length_pages()
					self.file_options()
		else:
			print('Такого файла не существует')
			self.main_menu()

	def contents(self):
		print('-----------------Оглавление------------------------')
		letters = {}
		for person in enumerate(self.telephone_directory, 1):
			letter = person[1][0]
			num_of_page = (person[0]-1)//10+1
			letters[letter] = letters.get(letter, num_of_page)
		for letter, number in letters.items():
			print(f'{letter}------------------------------------{number}')
		self.file_options()


	
	def open_page(self):
		self.opened_page = 1
		options = {
		'1': self.choose_page,
		'2': self.first_page,
		'4': self.file_options,
	}
		choices = [
			'1. Открыть страницу по номеру\n',
			'2. Открыть первую страницу\n',
			'3. Вернуться в главное меню\n',
			]
		choice = input(''.join(choices))
		options[choice]()

	def choose_page(self):
		num = int(input('Введите номер нужной вам страницы:\n'))
		if num <= 0 or num > self.pages:
			print('Такой страницы не существует')
			self.open_page()
		else:
			self.opened_page = num
			self.show_page()

	def show_page(self):
		print(f'--------------СТРАНИЦА_НОМЕР_{self.opened_page}---------------------')
		if self.opened_page*10+1 >= self.length:
			for person in self.telephone_directory[(self.opened_page-1)*10:]:
				print(person.rstrip())
		else:
			for person in self.telephone_directory[(self.opened_page-1)*10:self.opened_page*10]:
				print(person.rstrip())
		print()

		options = {
		'1': self.choose_page,
		'2': self.next_page,
		'3': self.file_options,
		}

		choices = [
			'1. Открыть страницу по номеру\n',
			'2. Открыть следующую страницу\n',
			'3. Вернуться в главное меню\n',
			]

		choice = input(''.join(choices))
		options[choice]()



	def first_page(self):
		self.opened_page = 1
		self.show_page()

	def next_page(self):
		if self.opened_page+1 > self.pages:
			print('Это последняя страница\n')
			self.open_page()
		else:
			self.opened_page += 1
			self.show_page()
		
	def length_pages(self):
		if self.length%10 == 0:
			self.pages = self.length//10
		else:
			self.pages = self.length//10 + 1

	def search_person(self):
		choices = [
			'1. Поиск по имени, фамилии или отчеству\n',
			'3. Поиск по организации\n',
			'4. Поиск по личному номеру телефона\n',
			'5. Поиск по рабочему номеру телефона\n',
			'6. Вернуться в главное меню\n',
			]
		choice = input(''.join(choices))
		if choice == '1':
			request = input('Введите фамилию, имя или отчество:\n')
			result = []
			for person in enumerate(self.telephone_directory ,1):
				temp_person = person[1].split(', ')[0].find(request)
				if temp_person != -1:
					result.append(person)
		elif choice == '3':
			request = input('Введите название организации:\n')
			result = []
			for person in enumerate(self.telephone_directory ,1):
				temp_person = person[1].split(', ')[1].find(request)
				if temp_person != -1:
					result.append(person)
		elif choice in '45':
			request = input('Введите номер телефона:\n')
			result = []
			if choice == 4:
				choice = 2
			else:
				choice = 3
			for person in enumerate(self.telephone_directory ,1):
				temp_person = person[1].split(', ')[choice].find(request)
				if temp_person != -1:
					result.append(person)
		else:
			self.file_options()
		if len(result) == 1 :
			print(f'{result[0][0]}. {result[0][1]}')
			self.chosen_person = result[0][0]-1
			self.choose_mode()
		elif len(result) > 1:
			print("По вашему запросу нашлось несколько записей:")
			for num, person in result:
				print(f'{num}. {person}')
			self.chosen_person = int(input('Выберите одну из записей для работы с ней:\n'))-1
			self.choose_mode()
		else:
			print('К сожалению, по вашему вопросу не удалось ничего найти')
			self.search_person()

	def edit_person(self):
		self.search_person()

		options = {
		'1': self.change_person,
		'2': self.delete_person,
		'3': self.search_person,
		'4': self.file_options,
		} 

		choices = [
			'1. Изменить данные в записи\n',
			'2. Удалить запись\n',
			'3. Вернуться к поиску записей\n',
			'4. Вернуться в главное меню\n',
			]

		choice = input(''.join(choices))
		options[choice]()

	def change_person(self):
		self.mode = 'change'
		if self.chosen_person == -1:
			self.search_person()
		self.mode = None
		self.telephone_directory.pop(self.chosen_person)
		print('Введите новые данные пользователя в формате:')
		person = input("Фамилия Имя Отчество, Организация, Личный номер телефона, Рабочий номер телефона\n")
		self.telephone_directory.append(person)
		self.chosen_person = ''
		self.write_changes()

	def delete_person(self):
		self.mode = 'delete'
		if self.chosen_person == -1:
			self.search_person()
		self.mode = None
		self.telephone_directory.pop(self.chosen_person)
		print('Запись была успешно удалена')
		self.write_changes()
		self.file_options()

	def write_changes(self):
		with open(self.file_name, 'w', encoding='utf-8') as file:
			write_list = [i+'\n' for i in sorted(set(self.telephone_directory))]
			print(write_list)
			file.writelines(write_list)
			file.flush()
		self.file_options()

	def choose_mode(self):
		if self.mode:
			self.mods[self.mode]()
		else:
			self.edit_person()

	def add_person(self):
		print('Введите данные нового пользователя в формате:')
		person = input("Фамилия Имя Отчество, Организация, Личный номер телефона, Рабочий номер телефона\n")
		self.telephone_directory.append(person)
		self.write_changes()
		self.file_options()
		







class DataFactory: # Создает тестовые данные

	def __init__(self, file_name, length=30): # принимает количество записей в телефонной книге
		self.length = int(length)
		self.fake = Faker('ru_RU')
		self.file_name = file_name + '.txt'
		self.creating_file()

	def creating_file(self):
		self.create_phones()
		self.create_companies()
		self.create_people()

		telephone_directory = []
		for name, tel1, tel2 in zip(self.people, self.personal_phones, self.work_phones):
			telephone_directory.append(', '.join((name, choice(self.companies), tel1, tel2))+'\n')
		self.telephone_directory = telephone_directory

		with open(self.file_name, 'w', encoding='utf-8') as tel:
			tel.writelines(sorted(set(self.telephone_directory)))

	def create_phones(self):
		phones = ['+7'+self.fake.numerify('(###)###-##-##') for _ in range(self.length*2)]
		self.personal_phones = phones[:self.length]
		self.work_phones = phones[self.length:]

	def create_companies(self):
		self.companies = [self.fake.company() for _ in range(self.length//3+1)]

	def create_people(self):
		self.people = [self.fake.name() for _ in range(self.length)]



a = TelephoneBook()