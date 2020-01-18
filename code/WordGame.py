class WordGame:
    def __init__(self, player_data: dict):
        self.player_data = player_data

    def act(self):
        pass

    @property
    def answer(self):
        return 'Привет, ШУЕ!'

    @property
    def end(self):
        return False
