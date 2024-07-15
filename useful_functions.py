import pymorphy3
morph = pymorphy3.MorphAnalyzer()

def have_sense(s, lists_of_key_words):
    lists_of_norm_forms = [[] for _ in range(len(lists_of_key_words))]
    for i in range(len(lists_of_key_words)):
        for w in lists_of_key_words[i]:
            lists_of_norm_forms[i] += [form.normal_form for form in morph.parse(w)]
    words = list(map(lambda s1: clear(s1), s.split()))
    input_norm_forms = []
    for w in words:
        input_norm_forms += [form.normal_form for form in morph.parse(w)]
    res = [len(set(input_norm_forms).intersection(set(list_of_norm_forms))) != 0 for list_of_norm_forms in lists_of_norm_forms]
    return res


def clear(s):
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
    s = s.lower().strip()
    s = "".join([c for c in s if c in alph])
    return s


def create_response(event, change_in_state=None, text="", buttons=None, end_session='false'):
    if change_in_state is None:
        change_in_state = {}
    if buttons is None:
        buttons = []
    session_state = event['state']['session']
    for prop in change_in_state:
        session_state[prop] = change_in_state[prop]
    tts = text
    if len(buttons) != 0:
        tts += " Варианты ответа: "
        for button in buttons:
            tts += button['title'] + ', '
        tts = tts[:-2]
        tts += '.'

    buttons += [
        {"title": 'Вернуться к вводу возраста', "payload": {}, "hide": "true"},
        {"title": 'Вернуться к выбору темы', "payload": {}, "hide": "true"},
    ]
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': session_state,
        'response': {
            'text': text,
            'tts': tts,
            'end_session': end_session,
            'buttons': buttons
        },
    }