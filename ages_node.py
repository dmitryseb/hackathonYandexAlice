from kids import request_kids
from teen import request_teens
from adults import request_adults
from useful_functions import create_response


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
        return request_kids(event, context, message)
    elif 12 <= age <= 16:
        return request_teens(event, context, message)
    elif 17 <= age <= 99:
        return request_adults(event, context, message)
    else:
        return create_response(event, {"value": "request_age"},
                               text="Я могу помочь с психологическими вопросами, которые тебя беспокоят. Прежде чем мы начнём, уточни, пожалуйста, сколько тебе лет?")
