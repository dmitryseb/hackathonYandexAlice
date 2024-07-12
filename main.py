import random
from teen import *

age = 0


def request_kids(event, context, message=""):
    text = "Хорошо! Давай поболтаем! Выбери, с чем я могу тебе помочь!"
    if message:
        text = message
    buttons = [{"title": "Отношения с мамой или папой"},
               {"title": "Школьные вопросы"},
               {"title": "Друзья"},
               {"title": "Самочувствие"},
               {"title": "Плохое настроение, давай поиграем в игру!"}]
    global age
    return {
        "version": event["version"],
        "session": event["session"],
        "session_state": {"value": "answer kids", "age": age},
        "response": {
            "text": text,
            "end_session": "false",
            "buttons": buttons
        },
    }


def answer_kids(event, context, message=""):
    answers = ["Отношения с мамой или папой".lower().split(),
               "Школьные вопросы".lower().split(),
               "Друзья".lower().split(), "Самочувствие".lower().split(),
               "Плохое настроение давай поиграем в игру".lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        if answers.index(event["request"]["nlu"]["tokens"]) == 4:
            event.pop("request")
            return relax_game(event, context, message)
        global age
        event["state"]["session"]["age"] = age
        return {
            "version": event["version"],
            "session": event["session"],
            "session_state": event["state"]["session"],
            "response": {
                "text": "выбран вариант номер " + str(answers.index(event["request"]["nlu"]["tokens"]) + 1),
                "end_session": "true"
            },
        }
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return request_kids(event, context, message)


def clear(s):
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "
    s = s.lower().strip()
    s = "".join([c for c in s if c in alph])
    return s


f = open('vegetables.txt', 'r')
vegetables = list(map(lambda s: clear(s), f.readlines()))
starts = ['А ты ', 'Ну ты и ', 'Вот ты ', 'Вот же ты ']


def relax_game(event, context, message=""):
    global age
    text = 'Привет! Давай поиграем в обзывашки: по очереди будем называть друг друга разными овощами. Если тебе ' \
           'наскучит, то ты всегда можешь написать: давай закончим. Я начну: Ты ' \
           'огурец! '
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        if "давай" in event['request']['original_utterance'].lower() and "закончим" in event['request'][
            'original_utterance'].lower():
            if 12 > age:
                return request_kids(event, context, message)
            elif 16 >= age:
                return request_teens(event, context, message)
            else:
                return request_adults(event, context, message)

        words = list(map(lambda s: clear(s), event['request']['original_utterance'].split()))
        ok = False
        for veg in vegetables:
            if veg in words:
                ok = True
                break
        if ok:
            text = random.choice(starts) + random.choice(vegetables) + '!'
        else:
            text = 'Ой, я не знаю такого овоща. Попробуй, например, вспомнить что-нибудь, что добавляют в твой ' \
                   'любимый суп. '
    return {
        'version': event['version'],
        'session': event['session'],
        "session_state": {"value": "relax game", "age": age},
        'response': {
            # Respond with the original request or welcome the user if this is the beginning of the dialog and the
            # request has not yet been made.
            'text': text,
            # Don't finish the session after this response.
            'end_session': 'false'
        },
    }


def request_adults(event, context, message=""):
    text = "Хорошо! Давайте поболтаем! Выберите, с чем я могу вам помочь!"
    if message:
        text = message
    buttons = [{"title": "Отношения с ребёнком"},
               {"title": "Его чувства и эмоции"}]
    global age
    return {
        "version": event["version"],
        "session": event["session"],
        "session_state": {"value": "answer adults", "age": age},
        "response": {
            "text": text,
            "end_session": "false",
            "buttons": buttons
        },
    }


def answer_adults(event, context, message=""):
    answers = ["Отношения с ребёнком".lower().split(),
               "Его чувства и эмоции".lower().split()]
    global age
    event["state"]["session"] = age

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        return {
            "version": event["version"],
            "session": event["session"],
            "session_state": {"value": "answer adults", "age": age},
            "response": {
                "text": "Извините, я пока не могу помочь с этим вопросом.",
            },
        }
    message = "Некорректный ответ. Пожалуйста, выберите другой вариант ответа"
    return request_adults(event, context, message)


def request_age(event, context, message=""):
    if "request" in event and "original_utterance" in event["request"] and len(
            event["request"]["original_utterance"]) and event["request"][
        "original_utterance"].isdigit():
        global age
        age = int(event["request"]["original_utterance"])
        if not 99 >= age >= 0:
            text = "Некорректный ответ. Пожалуйста, введите что-то другое."
            return {
                "version": event["version"],
                "session": event["session"],
                "session_state": event["state"]["session"],
                "response": {
                    "text": text,
                    "end_session": "false"
                },
            }
        if 12 > age:
            return request_kids(event, context, message)
        elif 16 >= age:
            return request_teens(event, context, message)
        else:
            return request_adults(event, context, message)
    text = "Некорректный ответ. Пожалуйста, введите что-то другое."
    return {
        "version": event["version"],
        "session": event["session"],
        "session_state": event["state"]["session"],
        "response": {
            "text": text,
            "end_session": "false"
        },
    }


functions = dict()
functions["request age"] = request_age
functions["answer kids"] = answer_kids
functions["answer adults"] = answer_adults
functions["relax game"] = relax_game
functions["teenagers_specify"] = teenagers_specify
functions['teenagers_friends'] = teenagers_friends
functions['teenagers_love'] = teenagers_love
functions['teenagers_bored'] = teenagers_bored
functions['request_teens'] = request_teens
functions['teenagers_enter2'] = teenagers_enter2


def handler(event, context):  # функция для точки входа
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    """Если состояние не является начальным, то вызываем побочную функцию"""
    if len(event['request']['original_utterance']) > 0:
        words = list(map(lambda s: clear(s), event['request']['original_utterance'].split()))
        key_words = ['помощь', 'помочь', 'уметь']
        res = False
        for w in words:
            if res:
                break
            forms = morph.parse(w)
            for form in forms:
                nform = form.normal_form
                if nform in key_words:
                    res = True
        if res:
            return {
                "version": event["version"],
                "session": event["session"],
                "session_state": {"value": "request age"},
                "response": {
                    "text": "Я могу помочь с психологическими вопросами, которые тебя беспокоят. Прежде чем мы начнём, уточни, пожалуйста, сколько тебе лет?",
                    "end_session": "false"
                },
            }
    if "value" in event["state"]["session"]:
        if event["state"]["session"]["value"] in functions.keys():
            if "age" in event["state"]["session"]:
                global age
                age = int(event["state"]["session"]["age"])
            return functions[event["state"]["session"]["value"]].__call__(event, context)
        else:
            return {
                "version": event["version"],
                "session": event["session"],
                "session_state": {},
                "response": {
                    "text": "Некорректное состояние",
                    "end_session": "true"
                },
            }

    text = "Привет! Я могу помочь с психологическими вопросами, которые тебя беспокоят. Прежде чем мы начнём, уточни, пожалуйста, сколько тебе лет?"
    return {
        "version": event["version"],
        "session": event["session"],
        "session_state": {"value": "request age"},
        "response": {
            "text": text,
            "end_session": "false"
        },
    }
