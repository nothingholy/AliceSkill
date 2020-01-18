import json


class Session:
    _session = dict()
    filename = "session_database.json"

    def __init__(self):
        # Открыли файл session_database.json на w (запись)
        with open(Session.filename, "w", encoding="utf8") as file:
            json.dump(self._session, fp=file)

    def load_session(self):
        with open(Session.filename, encoding="utf8") as file:
            self._session = json.loads(file.read())

        return self._session

    def save_session(self):
        with open(Session.filename, encoding="utf8") as file:
            json.dump(self._session, fp=file)
