from kids import request_kids
from teen import request_teens
from adults import request_adults
from useful_functions import create_response, extract_numbers


def request_age(event, context, message=""):
    text = "Пожалуйста, введите Ваш возраст (целое число от 0 до 99)."
    if message != "":
        text = message
    return create_response(event, change_in_state={"value": "proceed_age"}, text=text)


def proceed_age(event, context, message=""):
    if "request" in event and "original_utterance" in event["request"] and len(
            event["request"]["original_utterance"]):
        age = -1
        if "age" in event["state"]["session"]:
            age = event["state"]["session"]["age"]
        numbers = extract_numbers(event)
        if len(numbers) > 0:
            age = numbers[0]
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
    return request_age(event, context, message=message)


def show_manual(event, context, message=""):
    return create_response(event, change_in_state={"value": event["state"]["session"]["prev_value"]},
                           text="Я - индюк Брандуляк. Я могу помочь с психологическими вопросами, которые тебя беспокоят. "
                                "Чтобы ввести свой возраст, скажи \"Вернуться к вводу возраста\" или нажми кнопку снизу. "
                                "Чтобы выбрать тему для общения, скажи \"Вернуться к выбору темы\" или нажми кнопку снизу. "
                                "Чтобы продолжить общение, напиши \"Продолжить\" или что-нибудь другое."
                           )


def show_what_can_you_do(event, context, message=""):
    return create_response(event, change_in_state={"value": event["state"]["session"]["prev_value"]},
                           text="Я - индюк Брандуляк. Я могу помочь с психологическими вопросами, которые тебя беспокоят. Я умею давать советы, помогать в сложных ситуациях и даже играть в игры! "
                                "Чтобы продолжить общение, напиши \"Продолжить\" или что-нибудь другое."
                           )


def you_are_welcome(event, context, message=""):
    return create_response(event, change_in_state={"value": event["state"]["session"]["prev_value"]},
                           text="Всегда рад помочь!"
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
