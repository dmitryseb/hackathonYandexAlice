from relax_game import relax_game
from useful_functions import create_response
from school_game import school_game


def request_kids(event, context, message=""):
    text = "Хорошо! Давай поболтаем! Выбери, с чем я могу тебе помочь."
    if message:
        text = message
    buttons = [{"title": "Отношения с мамой или папой"},
               {"title": "Школа"},
               {"title": "Друзья"},
               {"title": "Самочувствие"},
               {"title": "Давай повеселимся!"}]
    return create_response(event, {"value": "answer_kids"}, text, buttons)


def answer_kids(event, context, message=""):
    answers = ["Отношения с мамой или папой".lower().split(),
               "Школа".lower().split(),
               "Друзья".lower().split(), "Самочувствие".lower().split(),
               "Плохое настроение давай поиграем в игру".lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        if answers.index(event["request"]["nlu"]["tokens"]) == 4:
            event.pop("request")
            return relax_game(event, context, message)
        elif answers.index(event["request"]["nlu"]["tokens"]) == 1:
            return school_questions(event, context)
        return create_response(event,
                               text="выбран вариант номер " + str(answers.index(event["request"]["nlu"]["tokens"]) + 1))
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return request_kids(event, context, message)


def school_questions(event, context, message=""):
    text = "Хорошо. Давай поговорим про школу. Вот, что я могу тебе предложить:"
    if message:
        text = message
    buttons = [{"title": "Поиграем в игру про школу"}]
    return create_response(event, {"value": "school_answers"}, text, buttons)


def school_answers(event, context, message=""):
    answers = ["Поиграем в игру про школу".lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        if answers.index(event["request"]["nlu"]["tokens"]) == 0:
            return school_game(event, context, message)
        return create_response(event,
                               text="выбран вариант номер " + str(answers.index(event["request"]["nlu"]["tokens"]) + 1))
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return request_kids(event, context, message)
