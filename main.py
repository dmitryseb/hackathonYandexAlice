import random
from teen import *
from useful_functions import create_response, have_sense, clear


def request_kids(event, context, message=""):
    text = "Хорошо! Давай поболтаем! Выбери, с чем я могу тебе помочь!"
    if message:
        text = message
    buttons = [{"title": "Отношения с мамой или папой"},
               {"title": "Школьные вопросы"},
               {"title": "Друзья"},
               {"title": "Самочувствие"},
               {"title": "Плохое настроение, давай поиграем в игру!"}]
    return create_response(event, {"value": "answer kids"}, text, buttons)


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
        return create_response(event, text="выбран вариант номер " + str(answers.index(event["request"]["nlu"]["tokens"]) + 1))
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return request_kids(event, context, message)


def relax_game(event, context, message=""):
    f = open('vegetables.txt', 'r')
    vegetables = list(map(lambda s: clear(s), f.readlines()))
    f.close()
    starts = ['А ты ', 'Ну ты и ', 'Вот ты ', 'Вот же ты ']
    text = 'Привет! Давай поиграем в обзывашки: по очереди будем называть друг друга разными овощами. Если тебе ' \
           'наскучит, то ты всегда можешь написать: давай закончим. Я начну: Ты ' \
           'огурец! '
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        if "давай" in event['request']['original_utterance'].lower() and "закончим" in event['request'][
            'original_utterance'].lower():
            age = int(event["state"]["session"]["age"])
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
    return create_response(event, {"value": "relax game"}, text)


def request_adults(event, context, message=""):
    text = "Хорошо! Давайте поболтаем! Выберите, с чем я могу вам помочь!"
    if message:
        text = message
    buttons = [{"title": "Отношения с ребёнком"},
               {"title": "Его чувства и эмоции"}]
    return create_response(event, {"value": "answer adults"}, text, buttons)


def answer_adults(event, context, message=""):
    answers = ["Отношения с ребёнком".lower().split(),
               "Его чувства и эмоции".lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        return create_response(event, {"value": "answer adults"}, "Извините, я пока не могу помочь с этим вопросом.")
    message = "Некорректный ответ. Пожалуйста, выберите другой вариант ответа"
    return request_adults(event, context, message)


def request_age(event, context, message=""):
    if "request" in event and "original_utterance" in event["request"] and len(
            event["request"]["original_utterance"]):
        age = -1
        if event["request"]["original_utterance"].isdigit():
            age = int(event["request"]["original_utterance"])
        elif "nlu" in event["request"] and "entities" in event["request"]["nlu"] and len(
                event["request"]["nlu"]["entities"]) and "value" in event["request"]["nlu"][
            "entities"][0] and event["request"]["nlu"]["entities"][0]["type"] == "YANDEX.NUMBER":

            age = event["request"]["nlu"]["entities"][0]["value"]
        event["state"]["session"]["age"] = age
        if not 0 <= age <= 99:
            text = "Пожалуйста, введите Ваш возраст (целое число от 0 до 99)."
            return create_response(event, text=text)
        if 0 <= age <= 11:
            return request_kids(event, context, message)
        elif 12 <= age <= 16:
            return request_teens(event, context, message)
        elif 17 <= age <= 99:
            return request_adults(event, context, message)
    text = "Пожалуйста, введите Ваш возраст (целое число от 0 до 99)."
    return create_response(event, text=text)


def show_manual(event, context, message=""):
    return create_response(event,
                           text="Я могу помочь с психологическими вопросами, которые тебя беспокоят. "
                                "Чтобы ввести свой возраст - скажи \"Заново\" или нажми кнопку снизу. "
                                "Чтобы выбрать тему для общения - скажи \"Выбор темы\" или нажми кнопку снизу. "
                           )


def show_what_can_you_do(event, context, message=""):
    return create_response(event,
                           text="Я могу помочь с психологическими вопросами, которые тебя беспокоят."
                           )


def show_topics(event, context, message=""):
    age = -1
    if "age" in event["state"]["session"]:
        age = int(event["state"]["session"]["age"])
    if 0 <= age <= 11:
        return request_kids(event, context)
    elif 12 <= age <= 16:
        return request_teens(event, context)
    elif 17 <= age <= 99:
        return request_adults(event, context)
    else:
        return create_response(event, {"value": "request age"},
                               text="Я могу помочь с психологическими вопросами, которые тебя беспокоят. Прежде чем мы начнём, уточни, пожалуйста, сколько тебе лет?")


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
functions["show_manual"] = show_manual
functions["show_what_can_you_do"] = show_what_can_you_do
functions["show_topics"] = show_topics


def check_reference(event):
    if len(event['request']['original_utterance']) > 0:
        key_words = [['помощь', 'помочь'],
                     ['уметь'],
                     ['вернуть', 'вернуться', 'покажи', 'возвращаться'],
                     ['тема', 'начало'],
                     ['возраст']]
        senses = have_sense(event['request']['original_utterance'], key_words)
        if senses[0]:
            event["state"]["session"]["value"] = "show_manual"
        elif senses[1]:
            event["state"]["session"]["value"] = "show_what_can_you_do"
        elif senses[2] and senses[3]:
            event["state"]["session"]["value"] = "show_topics"
        elif senses[2] and senses[4]:
            event["state"]["session"]["value"] = "request age"

def handler(event, context):  # функция для точки входа
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    """Если состояние не является начальным, то вызываем побочную функцию"""
    if 'original_utterance' not in event["request"]:
        if 'nlu' in event['request'] and 'tokens' in event["request"]["nlu"]:
            event["request"]["original_utterance"] = " ".join(event["request"]["nlu"]["tokens"])

    check_reference(event)

    if "value" in event["state"]["session"]:
        if event["state"]["session"]["value"] in functions.keys():
            res = functions[event["state"]["session"]["value"]].__call__(event, context)
            if "age" not in res["session_state"]:
                res["session_state"]["age"] = -1
            return res

        else:
            return create_response(event, text="Некорректное состояние", end_session='true')

    text = "Привет! Я могу помочь с психологическими вопросами, которые тебя беспокоят. Прежде чем мы начнём, уточни, пожалуйста, сколько тебе лет?"
    return create_response(event, {"value": "request age"}, text)