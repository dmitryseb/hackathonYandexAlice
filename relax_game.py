from useful_functions import clear, create_response, have_sense
import random

f = open('vegetables.txt', 'r', encoding="utf8")
vegetables = list(map(lambda s: clear(s), f.readlines()))
f.close()


def relax_game(event, context, message=""):
    global vegetables
    starts = ['А ты ', 'Ну ты и ', 'Вот ты ', 'Вот же ты ']
    text = 'Привет! Давай поиграем в обзывашки: по очереди будем называть друг друга разными овощами. Если тебе ' \
           'наскучит, то ты всегда можешь написать: давай закончим. А если нужна будет подсказка, так и скажи. Я начну: Ты ' \
           'огурец! '
    used_vegs = []
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        key_words = [['хватить', 'закончить', 'прекратить'],
                     ['подсказка', 'подсказать']]
        senses = have_sense(event['request']['original_utterance'], key_words)
        if 'used_vegs' in event['state']['session']:
            used_vegs = event['state']['session']['used_vegs']
        if senses[0]:
            return create_response(event, {"value": "show_topics"}, text="Хорошо, можем закончить. ")
        elif senses[1]:
            ans_veg = random.choice(vegetables)
            while ans_veg in used_vegs:
                ans_veg = random.choice(vegetables)
            text = "Знаешь, какой классный овощ я вспомнил? " + ans_veg.capitalize() + '!'
            return create_response(event, text=text)
        ok = False
        used_veg = ''
        for veg in vegetables:
            if have_sense(event['request']['original_utterance'], [[veg]])[0]:
                ok = True
                used_veg = veg
                break
        if ok:
            used_vegs.append(used_veg)
            ans_veg = random.choice(vegetables)
            while ans_veg in used_vegs:
                ans_veg = random.choice(vegetables)
            text = random.choice(starts) + ans_veg + '!'
        else:
            text = 'Ой, я не знаю такого овоща. Попробуй, например, вспомнить что-нибудь, что добавляют в твой ' \
                   'любимый суп. Или попроси подсказку. '
    return create_response(event, {"value": "relax_game", "used_vegs": used_vegs}, text, name_to_photo="relax_game")