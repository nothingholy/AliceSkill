import json


class AliceRequest:
    def __init__(self, request_json):
        request_dict = json.loads(request_json)

        self.version = request_dict['version']
        self.session = request_dict['session']
        self.user_id = request_dict['user_id']
        self.is_new_session = request_dict['is_new_session']
        self.command = request_dict['request']['command']


class AliceResponse:
    def __init__(self, alice_request: AliceRequest):
        self.response_dict = alice_request.__dict__.copy()

    def set_answer(self, text: str):
        self.response_dict['response']['text'] = text

    def set_end(self, state: bool):
        self.response_dict["response"]["end_session"] = state

    def __str__(self):
        return json.dumps(
            self.response_dict,
            ensure_ascii=False,
            indent=2
        )