from advices_stress import advices_str, additional_str
from useful_functions import create_response, remain_letters
import random

end_text = "Было приятно пообщаться"


def request_adults(event, context, message=""):
    text = "Хорошо! Давайте поболтаем! Выберите, с чем я могу вам помочь!"
    if message:
        text = message
    buttons = [{"title": "Отношения с ребёнком"},
               {"title": "Его чувства и эмоции"},
               {"title": "Как ребенку справиться со стрессом?"}]
    return create_response(event, {"value": "answer_adults"}, text, buttons)


def answer_adults(event, context, message=""):
    answers = ["Отношения с ребёнком".lower().split(),
               "Его чувства и эмоции".lower().split(),
               remain_letters("Как ребенку справиться со стрессом?").lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        if answers.index(event["request"]["nlu"]["tokens"]) == 2:
            return request_stress(event, context)
        return create_response(event, {"value": "answer_adults"},
                               text="Извините, пока я могу вам помочь только в случаях, описанных выше. Выберите из "
                                    "них, возможно, мой совет будет полезен.",
                               buttons=[{'title': "Как ребенку справиться со стрессом?"}
                                        ])

    message = "Пожалуйста, выберите из предложенных вариантов ответа."
    return request_adults(event, context, message)


def request_stress(event, context, message=""):
    text = "Понял, Вы хотите поговорить про стресс. Стресс — это состояние напряжения. Испытывать стресс — это нормально. Главное, быть рядом с ребенком и научить его справляться с этим состоянием. Хотите дам советы о том, как помочь ребенку справиться со стрессом?"
    if message:
        text = message
    return create_response(event, {"value": "adults_stress"}, text=text)


def adults_stress(event, context, message=""):
    if 'used_advices_str' not in event['state']['session']:
        event['state']['session']['used_advices_str'] = []
    if 'YANDEX.REJECT' in event['request']['nlu']['intents']:
        return create_response(event, {'value': 'request_adults'}, end_text)
    elif 'YANDEX.CONFIRM' not in event['request']['nlu']['intents']:
        return create_response(event, {'value': 'adults_stress'}, 'Извините, не понял. Вам нужен совет?')

    used_advices_str = event['state']['session']['used_advices_str']

    if 2 in used_advices_str and (
            not 'used_advices_str_add' in event['state']['session'] or len(
        event['state']['session']['used_advices_str_add']) != len(additional_str)):
        return request_add_stress(event, context, message)
    if len(used_advices_str) == len(advices_str):
        return create_response(event,
                               text="Дети с нейроотличиями могут переживать стрессовые ситуации сложнее. Больше "
                                    "информации о помощи детям в аутистическом спектре вы сможете узнать, например, "
                                    "на сайте благотворительного фонда Антон тут рядом, а если захотите пожертвовать "
                                    "средства в фонды, то сможете найти проверенные на сайте проекта Яндекса «Помощь "
                                    "рядом»." + end_text)

    advice_id = random.randint(0, len(advices_str) - 1)
    while advice_id in used_advices_str:
        advice_id = random.randint(0, len(advices_str) - 1)

    used_advices_str.append(advice_id)
    text = advices_str[advice_id]
    if advice_id != 2:
        text += '\nХотите ещё один совет?'
    return create_response(event, {
        'value': 'adults_stress',
        'used_advices_str': used_advices_str
    }, text, name_to_photo="adults")


def request_add_stress(event, context, message):
    if 'used_advices_str_add' not in event['state']['session']:
        event['state']['session']['used_advices_str_add'] = []
    used_advices_str = event['state']['session']['used_advices_str']
    used_advices_str_add = event['state']['session']['used_advices_str_add']
    advice_id = random.randint(0, len(additional_str) - 1)
    while advice_id in used_advices_str_add:
        advice_id = random.randint(0, len(additional_str) - 1)

    used_advices_str_add.append(advice_id)
    text = additional_str[advice_id]
    low_buttons = []
    if len(used_advices_str_add) != len(additional_str):
        low_buttons = [{"title": 'Да'}]
        text += '\nХотите расскажу еще про одно упражнение?'
    else:
        text += "\n На этом с упражнениями у меня все. Хотите дам еще один совет, связанный со стрессом?"
    return create_response(event, {
        'value': 'adults_stress',
        'used_advices_str': used_advices_str,
        'used_advices_str_add': used_advices_str_add
    }, text, name_to_photo="adults", low_buttons=low_buttons)
