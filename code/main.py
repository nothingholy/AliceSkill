from flask import Flask, request

from Alice import AliceRequest, AliceResponse
from Session import Session
from WordGame import WordGame

import config.local as config

app = Flask(__name__)
session = Session()


@app.route('/word-game/', methods=['POST'])
def word_game():
    alice_request = AliceRequest(request.json)

    temp_session = session.load_session()
    if alice_request.user_id not in temp_session:
        temp_session[alice_request.user_id] = dict()

    if temp_session[alice_request.user_id].get('end'):
        return ''

    game = WordGame(temp_session[alice_request.user_id])
    game.act(alice_request.command)

    alice_response = AliceResponse(alice_request)
    alice_response.set_answer(game.answer)
    alice_response.set_end(game.end)

    session.save_session()
    return str(alice_response)


if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT)
