import random

from bintrees import RBTree

word_tree = RBTree()
with open('dictionary.txt', 'r', encoding='utf8') as file:
    word_list = file.readlines()
    for line in word_list:
        word_tree.insert(line.rstrip(), True)


class WordGame:
    def __init__(self, player_data: dict):
        self.player_data = player_data

    def act(self):
        pass

    @property
    def answer(self):
        index = random.randint(0, len(word_list) - 1)
        return f'Привет, {word_list[index]}!'

    @property
    def end(self):
        return False
