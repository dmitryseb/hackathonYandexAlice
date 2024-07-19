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
    res = [len(set(input_norm_forms).intersection(set(list_of_norm_forms))) != 0 for list_of_norm_forms in
           lists_of_norm_forms]
    return res


def clear(s):
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
    s = s.lower().strip()
    s = "".join([c for c in s if c in alph])
    return s


def extract_numbers(event):
    res = set()
    if "nlu" in event["request"] and "entities" in event["request"]["nlu"]:
        for entity in event["request"]["nlu"]["entities"]:
            if entity["type"] == "YANDEX.NUMBER":
                res.add(int(entity["value"]))
    words = list(map(lambda s1: clear(s1), event["request"]["original_utterance"].split()))
    adjectives = {
        "первый": 1,
        "второй": 2,
        "третий": 3,
        "четвертый": 4,
        "четвёртый": 4,
        "пятый": 5,
        "шестой": 6,
        "седьмой": 7,
        "восьмой": 8,
        "девятый": 9,
        "десятый": 10,
    }
    for w in words:
        if w.isdigit():
            res.add(int(w))
    for adj in adjectives:
        if have_sense(event["request"]["original_utterance"], [[adj]])[0]:
            res.add(adjectives[adj])
    return list(res)


def remain_letters(s: str):
    res = ""
    for i in s:
        if i == " " or i.isalpha():
            res += i
    return res


photo_ids = dict()
photo_ids["relax_game"] = "13200873/a599c9b034f404575e46"
photo_ids["relationship"] = "213044/54b0a77551a367672dcf"
photo_ids["friends"] = "1521359/62ed0aa415f6607e6cdf"
photo_ids["advices"] = "997614/6f1586529c708c810b60"
photo_ids["school_game"] = "213044/eb72d04e42b2789b2ce6"
photo_ids["boring"] = "997614/f52f1a803dffc62753b6"
photo_ids["kids"] = "965417/b8d83841b0ed245ac3a0"
photo_ids["teens"] = "1652229/4d3a43434cae6ed274f6"
photo_ids["default"] = "965417/16b7f3b31462fdfd5d04"


def create_response(event, change_in_state=None, text="", buttons=None, end_session='false', name_to_photo="",
                    low_buttons=None):
    if change_in_state is None:
        change_in_state = {}
    if buttons is None:
        buttons = []
    if low_buttons is None:
        low_buttons = []
    session_state = event['state']['session']
    for prop in change_in_state:
        session_state[prop] = change_in_state[prop]
    tts = text
    session_state['prev_buttons'] = []
    if len(buttons) != 0:
        tts += " Варианты ответа: "
        num = 1
        for button in buttons:
            session_state['prev_buttons'].append(button['title'])
            tts += str(num) + ': ' + button['title'] + '. '
            num += 1

    for i in range(len(low_buttons)):
        low_buttons[i]["hide"] = "true"
    buttons += low_buttons
    buttons += [
        {"title": 'Вернуться к вводу возраста', "hide": "true"},
        {"title": 'Вернуться к выбору темы', "hide": "true"},
        {"title": 'Помощь', "hide": "true"},
    ]

    result = {
        'version': event['version'],
        'session': event['session'],
        'session_state': session_state,
        'response': {
            'text': text,
            'tts': tts,
            'end_session': end_session,
            'buttons': buttons,
        },
    }
    if name_to_photo in photo_ids:
        result["response"]["card"] = {'type': "BigImage", "image_id": photo_ids[name_to_photo], "description": text}
    elif "age" in result["session_state"]:
        age = int(result["session_state"]["age"])
        if 0 <= age <= 11:
            result["response"]["card"] = {'type': "BigImage", "image_id": photo_ids["kids"], "description": text}
        elif 12 <= age <= 99:
            result["response"]["card"] = {'type': "BigImage", "image_id": photo_ids["teens"], "description": text}
    else:
        result["response"]["card"] = {'type': "BigImage", "image_id": photo_ids["default"], "description": text}
    return result
