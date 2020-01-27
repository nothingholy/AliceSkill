## @package Session
## @brief Модуль, описывающий сохранение данных о сессии

import json


## Сессия и взаимодействие
class Session:
    _session = dict()

    ## Название файла с кэшированной сессией
    filename = 'session_database.json'

    ## Конструктор
    def __init__(self):
        # Открыли файл session_database.json на w (запись)
        with open(Session.filename, 'w', encoding='utf8') as file:
            json.dump(self._session, fp=file)

    ## Загрузить данные о сессии из файла
    def load_session(self):
        with open(Session.filename, 'r', encoding='utf8') as file:
            self._session = json.loads(file.read())

        return self._session

    ## Сохранить данные о сессии
    def save_session(self):
        with open(Session.filename, 'w', encoding='utf8') as file:
            json.dump(self._session, fp=file)
