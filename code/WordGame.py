## @package WordGame
## @brief Модуль, описывающий логику игры

import random

from bintrees import RBTree


## Коллекция слов (словарь и обработка)
class WordCollection:
    ## Список слов
    word_list = None

    ## Дерево поиска (RBTree)
    word_tree = None

    ## Конструктор
    def __init__(self):
        WordCollection.word_tree = RBTree()

        with open('dictionary.txt', 'r', encoding='utf8') as file:
            WordCollection.word_list = file.readlines()
            for line in WordCollection.word_list:
                WordCollection.word_tree.insert(line.rstrip(), True)

    ## Получение случайного слова из словаря
    ## @return Случайное слово из словаря
    @staticmethod
    def get_random_word():
        index = random.randint(0, len(WordCollection.word_list) - 1)
        return WordCollection.word_list[index].rstrip()

    ## Преобразование слова в словарь буква->количество
    ## @param word Слово
    ## @return Словарь
    @staticmethod
    def word_to_letters_dict(word):
        result = dict()
        for c in word:
            if c in result:
                result[c] += 1
            else:
                result[c] = 1

        return result

    ## Добавление случайного количества букв
    ## @param letters_dict Словарь буква->количество
    @staticmethod
    def add_letters(letters_dict: dict):
        keys = list(letters_dict.keys())  # Все ключи словаря (буквы слова, уникальные)

        keys_amount = random.randint(2, len(keys) - 1)  # Количество букв (уникальных), у которых увеличим количество
        for _ in range(0, keys_amount):
            letter = keys[random.randint(0, len(keys) - 1)]  # Случайная конкретная буква
            keys.remove(letter)  # Удаляем, чтобы не повторяться

            add_letter_amount = random.randint(1, 4)  # Количество добавленных букв
            letters_dict[letter] += add_letter_amount

    ## Находится ли слово в заданном словаре
    ## @param word Слово
    ## @param letters_dict_old Заданный словарь (не изменяется)
    ## @return True, если слово из заданного словаря
    @staticmethod
    def check_word_with_letters_dict(word: str, letters_dict_old: dict):
        letters_dict = letters_dict_old.copy()

        for letter in word.lower():  # Подсчет букв
            if letter not in letters_dict:
                return False  # Буквы нет в словаре - выход

            letters_dict[letter] -= 1
            if letters_dict[letter] < 0:
                return False

        return True


## Инициализация коллекции
collection = WordCollection()


## Класс логики игры
class WordGame:
    ## Данные об игроке
    player_data = None

    ## Подготовленный ответ
    prepared_answer = None

    ## Конструктор
    ## @param player_data Информация об игроке
    def __init__(self, player_data: dict):
        self.player_data = player_data
        self.prepared_answer = ''

        if 'letters' not in self.player_data:
            self.player_data['letters'] = dict()
            self.player_data['points'] = 0
            self.player_data['end'] = False

    ## Функция взаимодействия
    ## @param command Команда
    def act(self, command: str):
        if command == '':
            self.check_word('начать игру')
        else:
            self.check_word(command)

    ## Записывает в будущий ответ сообщение приветствия
    def greetings(self):
        self.prepared_answer += 'Добро пожаловать в игру "Магические слова".\n' \
                                'Я даю Вам список букв и их количество, ' \
                                'а Вы составляете слово из этих букв (необязательно использовать все).\n' \
                                'Если не получается составить слово, можете сказать "Пропустить ход"\n' \
                                'За каждое составленное слово Вы получите +1 балл, а за каждое пропущенное -1 балл.' \
                                'После каждого составленного слова список букв меняется\n' \
                                'Скажите "Закончить игру", чтобы закончить игру\n' \
                                'Примечание: слово должно состоять не менее, чем из 4-х букв\n'

    ## Записывает в будущий ответ заданный словарь
    def letters_message(self):
        letters = self.player_data['letters']

        # Собирает строку БУКВА: КОЛИЧЕСТВО и соединяет в сообщение
        format_strs = [f'{letter}: {letters[letter]}' for letter in letters]
        random.shuffle(format_strs)

        self.prepared_answer += '\n '.join(format_strs) + '\n'

    ## Функция получения нового случайного слова
    def generate_word(self):
        self.player_data['word'] = WordCollection.get_random_word()  # Сохраняем слово

        self.player_data['letters'] = WordCollection.word_to_letters_dict(self.player_data['word'])  # Парсим буквы
        WordCollection.add_letters(self.player_data['letters'])  # Добавляем буквы

    ## Записывает в будущий ответ сообщение окончания
    def goodbye(self):
        self.prepared_answer += 'Вы закончили игру'

    ## Записывает в будущий ответ сообщение о количестве баллов
    def result_message(self):
        self.prepared_answer += f'Ваше текущее количество баллов: {self.player_data["points"]}\n'

    ## Проверка слова или команды
    ## @param command Команда
    def check_word(self, command: str):
        if command.lower() == 'пропустить ход':
            self.prepared_answer += f'Вы пропустили ход. Было загадано слово {self.player_data["word"]}\n'

            self.player_data['points'] -= 1
            self.result_message()

            self.generate_word()
            self.letters_message()

        elif command.lower() == 'начать игру':
            self.greetings()
            self.generate_word()
            self.letters_message()

            self.player_data['points'] = 0
            self.player_data['end'] = False

        elif command.lower() == 'закончить игру':
            self.goodbye()

            self.player_data['end'] = True

        else:
            if command not in WordCollection.word_tree:
                self.prepared_answer += 'Такого слова, увы, нет\n'
                return

            if not WordCollection.check_word_with_letters_dict(command, self.player_data['letters']):
                self.prepared_answer += 'У меня нет столько букв\n'
                return

            self.prepared_answer += 'Отличная работа'
            if command.lower() != self.player_data['word']:
                self.prepared_answer += f', но было загадано слово "{self.player_data["word"]}"'
            self.prepared_answer += '\n'

            self.player_data['points'] += 1
            self.result_message()

            self.generate_word()
            self.letters_message()

    ## Ответ
    @property
    def answer(self):
        return self.prepared_answer

    ## Окончена ли сессия
    @property
    def end(self):
        return self.player_data['end']
