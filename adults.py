from useful_functions import create_response


def request_adults(event, context, message=""):
    text = "Хорошо! Давайте поболтаем! Выберите, с чем я могу вам помочь!"
    if message:
        text = message
    buttons = [{"title": "Отношения с ребёнком"},
               {"title": "Его чувства и эмоции"}]
    return create_response(event, {"value": "answer_adults"}, text, buttons)


def answer_adults(event, context, message=""):
    answers = ["Отношения с ребёнком".lower().split(),
               "Его чувства и эмоции".lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        return create_response(event, {"value": "answer_adults"}, "Извините, я пока не могу помочь с этим вопросом.")
    message = "Некорректный ответ. Пожалуйста, выберите другой вариант ответа"
    return request_adults(event, context, message)


