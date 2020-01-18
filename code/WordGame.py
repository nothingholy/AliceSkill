import random

from bintrees import RBTree


class WordCollection:
    word_list = None
    word_tree = None

    def __init__(self):
        WordCollection.word_tree = RBTree()

        with open('dictionary.txt', 'r', encoding='utf8') as file:
            WordCollection.word_list = file.readlines()
            for line in WordCollection.word_list:
                WordCollection.word_tree.insert(line.rstrip(), True)

    @staticmethod
    def get_random_word():
        index = random.randint(0, len(WordCollection.word_list) - 1)
        return WordCollection.word_list[index].rstrip()

    @staticmethod
    def word_to_letters_dict(word):
        result = dict()
        for c in word:
            if c in result:
                result[c] += 1
            else:
                result[c] = 1

        return result

    @staticmethod
    def add_letters(letters_dict: dict):
        # TODO: variant, add new letters
        keys = list(letters_dict.keys())  # Все ключи словаря (буквы слова, уникальные)

        keys_amount = random.randint(2, len(keys) - 1)  # Количество букв (уникальных), у которых увеличим количество
        for _ in range(0, keys_amount):
            letter = keys[random.randint(0, len(keys) - 1)]  # Случайная конкретная буква
            keys.remove(letter)  # Удаляем, чтобы не повторяться

            add_letter_amount = random.randint(1, 4)  # Количество добавленных букв
            letters_dict[letter] += add_letter_amount

    @staticmethod
    def check_word_with_letters_dict(word: str, letters_dict_old: dict):
        letters_dict = letters_dict_old.copy()

        for letter in word:  # Подсчет букв
            if letter not in letters_dict:
                return False  # Буквы нет в словаре - выход

            letters_dict[letter] -= 1
            if letters_dict[letter] < 0:
                return False

        return True


collection = WordCollection()


class WordGame:
    def __init__(self, player_data: dict):
        self.player_data = player_data
        self.prepared_answer = ''

        if 'letters' not in self.player_data:
            self.player_data['letters'] = dict()
            self.player_data['points'] = 0
            self.player_data['end'] = False

    def act(self, command: str):
        if command == '':
            self.greetings()
            self.generate_word()
            self.letters_message()
        else:
            self.check_word(command)

    def greetings(self):
        self.prepared_answer += 'Добро пожаловать в игру "Магические слова".\n' \
                                'Я даю Вам список букв и их количество, ' \
                                'а Вы составляете слово из этих букв (необязательно использовать все).\n' \
                                'Если не получается составить слово, можете сказать "Пропустить ход"\n' \
                                'За каждое составленное слово Вы получите +1 балл, а за каждое пропущенное -1 балл.' \
                                'После каждого составленного слова список букв меняется\n' \
                                'Скажите "Закончить игру", чтобы закончить игру\n\n'

    def letters_message(self):
        letters = self.player_data['letters']

        # Собирает строку БУКВА: КОЛИЧЕСТВО и соединяет в сообщение
        format_strs = [f'{letter}: {letters[letter]}' for letter in letters]
        random.shuffle(format_strs)

        self.prepared_answer += '\n '.join(format_strs) + '\n'

    def generate_word(self):
        self.player_data['word'] = WordCollection.get_random_word()  # Сохраняем слово

        self.player_data['letters'] = WordCollection.word_to_letters_dict(self.player_data['word'])  # Парсим буквы
        WordCollection.add_letters(self.player_data['letters'])  # Добавляем буквы

    def goodbye(self):
        self.prepared_answer += 'Вы закончили игру'

    def result_message(self):
        self.prepared_answer += f'Ваше текущее количество баллов: {self.player_data["points"]}\n'

    def check_word(self, command: str):
        if command.lower() == 'пропустить ход':
            self.prepared_answer += f'Вы пропустили ход. Было загадано слово {self.player_data["word"]}\n'

            self.player_data['points'] -= 1
            self.result_message()

            self.generate_word()
            self.letters_message()

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

            self.prepared_answer += 'Отличная работа\n'

            self.player_data['points'] += 1
            self.result_message()

            self.generate_word()
            self.letters_message()

    @property
    def answer(self):
        return self.prepared_answer

    @property
    def end(self):
        return self.player_data['end']
