from Session import Session
from WordGame import WordCollection


def test_session_create():
    session = Session()

    assert type(session._session) == dict
    assert len(session._session) == 0


def test_session_save_and_load():
    session = Session()
    session._session['key1'] = 'value1'
    session._session['key2'] = 2

    session.save_session()

    new_session = Session()
    data = new_session.load_session()

    assert data['key1'] == 'value1'
    assert data['key2'] == 2


def test_word_to_letters():
    data = WordCollection.word_to_letters_dict('verylongword')

    assert type(data) == dict
    assert data['v'] == 1
    assert data['e'] == 1
    assert data['r'] == 2
    assert data['y'] == 1
    assert data['l'] == 1
    assert data['o'] == 2
    assert data['n'] == 1
    assert data['g'] == 1
    assert data['w'] == 1
    assert data['d'] == 1


def test_static_fields():
    assert len(WordCollection.word_list) == 2

    assert WordCollection.word_list[0].rstrip() == 'слово'
    assert WordCollection.word_list[1].rstrip() == 'другоеслово'


def test_add_letters():
    data = dict(a=1, b=1, c=1)
    WordCollection.add_letters(data)

    assert len(data) == 3

    assert data['a'] >= 1
    assert data['b'] >= 1
    assert data['c'] >= 1


def test_check_word_with_letters_dict_correct():
    data = dict(a=1, b=1, c=1)
    assert WordCollection.check_word_with_letters_dict('cAb', data) is True


def test_check_word_with_letters_dict_bad():
    data = dict(a=1, b=1, c=1)
    assert WordCollection.check_word_with_letters_dict('cAbb', data) is False
