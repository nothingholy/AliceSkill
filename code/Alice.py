## @package Alice
## @brief Модуль, описывающий классы, связанные с запросами к Алисе

import json


## Класс запроса от алисы
class AliceRequest:
    ## Версия API
    version = None

    ## Информация о сессии
    session = None

    ## Идентификатор пользователя
    user_id = None

    ## Является ли сессия новой
    is_new_session = None

    ## Текст команды
    command = None

    ## Конструктор
    ## @param request_dict Словарь запроса
    def __init__(self, request_dict: dict):
        self.version = request_dict['version']

        self.session = request_dict['session']
        self.user_id = self.session['user_id']
        self.is_new_session = self.session['new']

        self.command = request_dict['request']['command']


## Класс ответа Алисе
class AliceResponse:
    ## Словарь, содержащий информацию об ответе
    response_dict = None

    ## Конструктор
    ## @param alice_request Объект запроса
    def __init__(self, alice_request: AliceRequest):
        self.response_dict = alice_request.__dict__.copy()

        if 'response' not in self.response_dict:
            self.response_dict['response'] = dict()

    ## Установка ответа
    ## @param text Текст ответа
    def set_answer(self, text: str):
        self.response_dict['response']['text'] = text

    ## Установка окончания сессии
    ## @param state Состояние (True - окончание, иначе - False)
    def set_end(self, state: bool):
        self.response_dict['response']['end_session'] = state

    ## Преобразование в строку
    ## @return Строка
    def __str__(self):
        return json.dumps(
            self.response_dict,
            ensure_ascii=False,
            indent=2
        )
