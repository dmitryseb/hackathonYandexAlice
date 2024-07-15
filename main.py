from adults import answer_adults
from ages_node import request_age, show_manual, show_what_can_you_do, show_topics
from kids import school_answers, request_kids, answer_kids
from relax_game import relax_game
from teen import *
from useful_functions import create_response, have_sense
from school_game import school_game, begin_type, chill_start, urok, contra, obyasn, dz

functions = dict()
functions["request_age"] = request_age
functions["answer_kids"] = answer_kids
functions["answer_adults"] = answer_adults
functions["relax_game"] = relax_game
functions["teenagers_specify"] = teenagers_specify
functions['teenagers_friends'] = teenagers_friends
functions['teenagers_love'] = teenagers_love
functions['teenagers_bored'] = teenagers_bored
functions['request_teens'] = request_teens
functions["request_kids"] = request_kids
functions['teenagers_enter2'] = teenagers_enter2
functions["show_manual"] = show_manual
functions["show_what_can_you_do"] = show_what_can_you_do
functions["show_topics"] = show_topics
functions["school_game"] = school_game
functions["school_answers"] = school_answers
functions["begin_type"] = begin_type
functions["chill_start"] = chill_start
functions["urok"] = urok
functions["contra"] = contra
functions["obyasn"] = obyasn
functions["dz"] = dz


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
            event["state"]["session"]["value"] = "request_age"


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
    return create_response(event, {"value": "request_age"}, text)
