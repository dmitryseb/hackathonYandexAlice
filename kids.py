from relax_game import relax_game
from useful_functions import create_response, clear
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
    answers = ["Отношения с мамой или папой",
               "Школа",
               "Друзья", "Самочувствие",
               "Давай повеселимся!"]

    res = -1
    if "request" in event and "original_utterance" in event["request"]:
        for i in range(len(answers)):
            if clear(answers[i]) == clear(event["request"]["original_utterance"]):
                res = i
                break
    if res == 4:
        event.pop("request")
        return relax_game(event, context, message)
    elif res == 1:
        return school_questions(event, context)
    elif res == -1:
        message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
        return request_kids(event, context, message)
    return create_response(event,
                           text="Извини, пока я могу тебе помочь только в случаях, описанных выше. Выбери из них, возможно, мой совет будет полезен.",
                           buttons=[{"title": "Школа"},
                                    {'title': "Давай повеселимся!"},
                                    ])


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
    return school_questions(event, context, message)
