import random
from advice_friendship import advices_fr
from advice_bored import advices_br
from useful_functions import create_response, have_sense, clear

end_text = "Было приятно пообщаться. Удачи тебе! Оставайся радостными человеком и приятным собеседником."


def request_teens(event, context, message=''):
    text = 'Хорошо! Давай поговорим! Выбери, с чем я могу тебе помочь.'
    if message != '':
        text = message
    buttons = [
        {'title': 'Отношения с родителями'},
        {'title': 'Школа'},
        {'title': 'Друзья'},
        {'title': 'Отношения'},
        {'title': 'Эмоции'},
    ]
    return create_response(event, {'value': 'teenagers_enter2'}, text, buttons)


def teenagers_enter2(event, context):
    subtopics = ['Отношения с родителями', 'Школа', 'Друзья', 'Отношения', 'Эмоции']
    key_words = [['родители', 'мама', 'папа', 'отец', 'мать'],
                 ['школа'],
                 ['друг', 'дружба'],
                 ['отношения'],
                 ['эмоции', 'чувства']]
    senses = have_sense(event['request']['original_utterance'], key_words)
    if True not in senses:
        return request_teens(event, context, message='Выбери, пожалуйста, наиболее подходящую тему из списка.')
    else:
        subtopic = subtopics[senses.index(True)]
        text = 'Можешь рассказать о проблеме побольше?'
        return create_response(event, {
            'value': 'teenagers_specify',
            'subtopic': subtopic,
        }, text)


def teenagers_specify(event, context):
    subtopic = event['state']['session']['subtopic']
    key_words = [['друг', 'дружба', 'дружить'],
                 ['любовь', 'любить', 'отношения', 'парень', 'девушка', 'расставание', 'расстаться', 'бросить'],
                 ['скучно', 'скучать', 'скука', 'нечего', 'нечем']]
    senses = have_sense(event['request']['original_utterance'], key_words)
    text = 'Извини, я пока не смогу поддержать разговор на эту тему. ' \
           'Вот примеры вопросов, с которыми я могу помочь: как найти друзей, как решить проблему в отношениях или что делать, если скучно.'
    value = 'teenagers_specify'
    buttons = []
    if senses[0]:
        value = 'teenagers_friends_inter'
        text = 'Понял, тебя интересует, как найти друзей. ' \
               'Как ты думаешь, что такое дружба?'
    elif senses[1]:
        value = 'teenagers_love'
        text = 'Понял, ты хочешь поговорить об отношениях. Пожалуйста, выбери свой случай из списка.'
        buttons = [
            {'title': 'Мне нравится человек, а я ему нет'},
            {'title': 'Я нравлюсь человеку, а он мне нет'},
            {'title': 'У меня проблемы с моим партнёром'},
            {'title': 'Другой случай'},
        ]
    elif senses[2]:
        value = 'teenagers_bored'
        text = 'Понял, тебе скучно. Каждый отдыхает по-своему! Можно отдыхать с друзьями или одному. Скучно бывает всем и это не беда! ' \
               'Хочешь идею, чем заняться?'
    return create_response(event, {
        'value': value,
        'subtopic': subtopic
    }, text, buttons)


def teenagers_friends_inter(event, context):
    text = 'Дружба – это регулярное общение и взаимопонимание. ' \
               'Старайся быть откровенным и честным, и ты обязательно найдёшь настоящих друзей. ' \
               'Хочешь, я дам тебе совет, как это сделать?'
    return create_response(event, {
        'value': 'teenagers_friends'
    }, text, low_buttons=[{"title": 'Да'}])


def teenagers_friends(event, context):
    if 'used_advices_fr' not in event['state']['session']:
        event['state']['session']['used_advices_fr'] = []
    if 'YANDEX.REJECT' in event['request']['nlu']['intents']:
        return create_response(event, {'value': 'request_teens'}, end_text)
    elif 'YANDEX.CONFIRM' not in event['request']['nlu']['intents']:
        return create_response(event, {'value': 'teenagers_friends'}, 'Извини, не понял. Тебе нужен совет?')
    used_advices_fr = event['state']['session']['used_advices_fr']
    if len(used_advices_fr) == len(advices_fr):
        return create_response(event, text="Извини, советы закончились. " + end_text)
    advice_id = random.randint(0, len(advices_fr) - 1)
    while advice_id in used_advices_fr:
        advice_id = random.randint(0, len(advices_fr) - 1)
    used_advices_fr.append(advice_id)
    text = advices_fr[advice_id]
    low_buttons = []
    if len(used_advices_fr) != len(advices_fr):
        text += '\nХочешь ещё один совет?'
        low_buttons = [{"title": 'Да'}]
    return create_response(event, {
        'value': 'teenagers_friends',
        'used_advices_fr': used_advices_fr
    }, text, name_to_photo="friends", low_buttons=low_buttons)


def teenagers_love(event, context, message=''):
    response = clear(event['request']['original_utterance'])
    if response == 'другой случай':
        return create_response(event,
                               text="Извини, пока я могу тебе помочь, только в случаях, описанных выше. Выбери из них, возможно, мой совет будет полезен.",
                               buttons=[
                                   {'title': 'Мне нравится человек, а я ему нет'},
                                   {'title': 'Я нравлюсь человеку, а он мне нет'},
                                   {'title': 'У меня проблемы с моим партнёром'},
                               ])
    if response not in ['мне нравится человек а я ему нет', 'я нравлюсь человеку а он мне нет',
                        'у меня проблемы с моим партнёром']:
        return create_response(event,
                               text="Пожалуйста, выбери из предложенных вариантов. ",
                               buttons=[
                                   {'title': 'Мне нравится человек, а я ему нет'},
                                   {'title': 'Я нравлюсь человеку, а он мне нет'},
                                   {'title': 'У меня проблемы с моим партнёром'},
                                   {'title': 'Другой случай'},
                               ])
    text = ''
    if response == 'мне нравится человек а я ему нет':
        text = 'Не всегда мы можем понравиться другому человеку, и это нормально. Мы все разные и классные по-своему. Каждый из нас встретит того, кто ему подходит в правильное время. Если кто-то не оценил тебя так, как тебе бы хотелось, это не значит, что с тобой что-то не так. Просто ещё не пришло твоё время и не встретился твой человек.'
    elif response == 'я нравлюсь человеку а он мне нет':
        text = 'Не нужно чувствовать себя виноватым из-за этого. Не стоит начинать отношения из чувства жалости или вины. Ты не ответственен за чувства другого человека. Важно найти человека, с которым чувства будут взаимными. Взаимные чувства - это когда люди испытывают к нам ту же эмоцию, что и мы к ним. Бывает, что чувства не взаимны. Когда мы испытываем к людям одну эмоцию, а они к нам совсем другую. Это может быть печально, но жизнь такая.'
    elif response == 'у меня проблемы с моим партнёром':
        text = 'Обсуди открыто проблемы с партнёром. Попробуйте найти компромисс. Компромисс – это решение конфликта, которое устраивает вас обоих. Иногда нужно отказаться от части своих требований, чтобы прийти к компромиссу. Иногда конфликты бывают такими серьёзными, что нужно расстаться. Расставаться нормально. Можно обсудить проблему с близким человеком. Важно уважать и поддерживать друг друга.'
    return create_response(event, text=text, name_to_photo="relationship")


def teenagers_bored(event, context):
    if 'used_advices_br' not in event['state']['session']:
        event['state']['session']['used_advices_br'] = []
    if 'YANDEX.REJECT' in event['request']['nlu']['intents']:
        return create_response(event, {'value': 'request_teens'}, end_text)
    elif 'YANDEX.CONFIRM' not in event['request']['nlu']['intents']:
        return create_response(event, {'value': 'teenagers_friends'}, 'Извини, не понял. Тебе нужна идея?')
    used_advices_br = event['state']['session']['used_advices_br']
    if len(used_advices_br) == len(advices_br):
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Извини, идеи закончились. " + end_text,
                'end_session': 'false'
            },
        }
    advice_id = random.randint(0, len(advices_br) - 1)
    while advice_id in used_advices_br:
        advice_id = random.randint(0, len(advices_br) - 1)
    used_advices_br.append(advice_id)
    text = advices_br[advice_id]
    low_buttons = []
    if len(used_advices_br) != len(advices_br):
        text += '\nХочешь ещё одну идею?'
        low_buttons = [{"title": 'Да'}]
    return create_response(event, {
        'value': 'teenagers_bored',
        'used_advices_fr': used_advices_br
    }, text, name_to_photo="boring", low_buttons=low_buttons)
