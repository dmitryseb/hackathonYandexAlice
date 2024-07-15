from useful_functions import clear, create_response
import random


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
            return create_response(event, {"value": "show_topics"}, text="Хорошо, можем закончить. ")

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
    return create_response(event, {"value": "relax_game"}, text)
