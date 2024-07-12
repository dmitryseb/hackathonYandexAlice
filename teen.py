import random
import pymorphy3
from advice_friendship import advices_fr
from advice_bored import advices_br

morph = pymorphy3.MorphAnalyzer()
end_text = "Было приятно пообщаться. Удачи тебе! Оставайся радостными человеком и приятным собеседником."


def clear(s):
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "
    s = s.lower().strip()
    s = "".join([c for c in s if c in alph])
    return s


def request_teens(event, context, message=''):
    text = 'Хорошо! Давай поговорим! Выбери, с чем я могу тебе помочь!'
    if message != '':
        text = message
    buttons = [
        {'title': 'Отношения с родителями'},
        {'title': 'Школа'},
        {'title': 'Друзья'},
        {'title': 'Отношения'},
        {'title': 'Эмоции'},
    ]
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {
            'value': 'teenagers_enter2'
        },
        'response': {
            'text': text,
            'end_session': 'false',
            'buttons': buttons
        },
    }


def teenagers_enter2(event, context):
    response = event['request']['original_utterance']
    subtopic = ''
    value = 'request_teens'
    if response not in ['Отношения с родителями', 'Школа', 'Друзья', 'Отношения', 'Эмоции']:
        return request_teens(event, context, message='Выбери, пожалуйста, наиболее подходящую тему из списка.')
    else:
        subtopic = response
        text = 'Можешь рассказать немного больше о проблеме?'
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': 'teenagers_specify',
                'subtopic': subtopic,
            },
            'response': {
                'text': text,
                'end_session': 'false'
            },
        }


def teenagers_specify(event, context):
    subtopic = event['state']['session']['subtopic']
    words = list(map(lambda s: clear(s), event['request']['original_utterance'].split()))
    key_words1 = ['друг', 'дружба', 'дружить']
    key_words2 = ['любовь', 'любить', 'отношения', 'парень', 'девушка', 'расставание', 'расстаться', 'бросить']
    key_words3 = ['скучно', 'скучать', 'скука', 'нечего', 'нечем']
    res = -1
    for w in words:
        """if res != -1:
            break
        if w in key_words1:
            res = 1
        elif w in key_words2:
            res = 2
        elif w in key_words3:
            res = 3"""
        forms = morph.parse(w)
        for form in forms:
            nform = form.normal_form
            if nform in key_words1:
                res = 1
            elif nform in key_words2:
                res = 2
            elif nform in key_words3:
                res = 3
    text = 'Извини, я пока не смогу поддержать разговор на эту тему. ' \
           'Вот примеры вопросов, с которыми я могу помочь: как найти друзей, как решить проблему в отношениях или что делать, если скучно.'
    value = 'teenagers_specify'
    buttons = []
    if res == 1:
        value = 'teenagers_friends'
        text = 'Поняла, тебя интересует, как найти друзей. ' \
               'Давай разберёмся, что такое дружба? Дружба – это регулярное общение и взаимопонимание. ' \
               'Старайся быть откровенным и честным, и ты обязательно найдёшь настоящих друзей. ' \
               'Хочешь, я дам тебе совет, как это сделать?'
    elif res == 2:
        value = 'teenagers_love'
        text = 'Поняла, ты хочешь поговорить об отношениях. Пожалуйста, выбери свой случай из списка.'
        buttons = [
            {'title': 'Мне нравится человек, а я ему нет'},
            {'title': 'Я нравлюсь человеку, а он мне нет'},
            {'title': 'У меня проблемы с моим партнёром'},
            {'title': 'Другой случай'},
        ]
    elif res == 3:
        value = 'teenagers_bored'
        text = 'Поняла, тебе скучно. Каждый отдыхает по-своему! Можно отдыхать с друзьями или одному. Скучно бывает всем и это не беда! ' \
               'Хочешь идею, чем заняться?'
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {
            'value': value,
            'subtopic': subtopic
        },
        'response': {
            'text': text,
            'end_session': 'false',
            'buttons': buttons
        },
    }


def teenagers_friends(event, context):
    if 'YANDEX.REJECT' in event['request']['nlu']['intents']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': 'request_teens',
                'subtopic': event['state']['session']['subtopic']
            },
            'response': {
                'text': end_text,
                'end_session': 'true'
            },
        }
    elif 'YANDEX.CONFIRM' not in event['request']['nlu']['intents']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': 'teenagers_friends',
                'subtopic': event['state']['session']['subtopic']
            },
            'response': {
                'text': 'Извини, не поняла. Тебе нужен совет?',
                'end_session': 'false'
            },
        }
    advice = random.choice(advices_fr)
    text = advice + '\nХочешь ещё один совет?'
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {
            'value': 'teenagers_friends',
            'subtopic': event['state']['session']['subtopic']
        },
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }


def teenagers_love(event, context, message=''):
    response = event['request']['original_utterance']
    if response == 'Другой случай':
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': event['state']['session']['value'],
                'subtopic': event['state']['session']['subtopic']
            },
            'response': {
                'text': 'Извини, пока я могу тебе помочь, только в случаях, описанных выше. Выбери из них, возможно, мой совет будет полезен:',
                'end_session': 'false',
                'buttons': [
                    {'title': 'Мне нравится человек, а я ему нет'},
                    {'title': 'Я нравлюсь человеку, а он мне нет'},
                    {'title': 'У меня проблемы с моим партнёром'},
                ]
            },
        }
    if response not in ['Мне нравится человек, а я ему нет', 'Я нравлюсь человеку, а он мне нет', 'У меня проблемы с моим партнёром']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': event['state']['session']['value'],
                'subtopic': event['state']['session']['subtopic']
            },
            'response': {
                'text': 'Пожалуйста, выбери из предложенных вариантов:',
                'end_session': 'false',
                'buttons': [
                    {'title': 'Мне нравится человек, а я ему нет'},
                    {'title': 'Я нравлюсь человеку, а он мне нет'},
                    {'title': 'У меня проблемы с моим партнёром'},
                    {'title': 'Другой случай'},
                ]
            },
        }
    text = ''
    if response == 'Мне нравится человек, а я ему нет':
        text = 'Не всегда мы можем понравиться другому человеку, и это нормально. Мы все разные и классные по-своему. Каждый из нас встретит того, кто ему подходит в правильное время. Если кто-то не оценил тебя так, как тебе бы хотелось, это не значит, что с тобой что-то не так. Просто ещё не пришло твоё время и не встретился твой человек.'
    elif response == 'Я нравлюсь человеку, а он мне нет':
        text = 'Не нужно чувствовать себя виноватым из-за этого. Не стоит начинать отношения из чувства жалости или вины. Ты не ответственен за чувства другого человека. Важно найти человека, с которым чувства будут взаимными. Взаимные чувства - это когда люди испытывают к нам ту же эмоцию, что и мы к ним. Бывает, что чувства не взаимны. Когда мы испытываем к людям одну эмоцию, а они к нам совсем другую. Это может быть печально, но жизнь такая.'
    elif response == 'У меня проблемы с парнем/девушкой':
        text = 'Обсуди открыто проблемы с партнёром. Попробуйте найти компромисс. Компромисс – это решение конфликта, которое устраивает вас обоих. Иногда нужно отказаться от части своих требований, чтобы прийти к компромиссу. Иногда конфликты бывают такими серьёзными, что нужно расстаться. Расставаться нормально. Можно обсудить проблему с близким человеком. Важно уважать и поддерживать друг друга.'
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'true'
        },
    }


def teenagers_bored(event, context):
    if 'YANDEX.REJECT' in event['request']['nlu']['intents']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': 'request_teens',
                'subtopic': event['state']['session']['subtopic']
            },
            'response': {
                'text': end_text,
                'end_session': 'true'
            },
        }
    elif 'YANDEX.CONFIRM' not in event['request']['nlu']['intents']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {
                'value': 'teenagers_bored',
                'subtopic': event['state']['session']['subtopic']
            },
            'response': {
                'text': 'Извини, не поняла. Тебе нужен совет?',
                'end_session': 'false'
            },
        }
    advice = random.choice(advices_br)
    text = advice + '\nХочешь ещё одну идею?'
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {
            'value': 'teenagers_bored',
            'subtopic': event['state']['session']['subtopic']
        },
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }


def handler(event, context):
    dict_funcs = {
        'teenagers_specify': teenagers_specify,
        'teenagers_friends': teenagers_friends,
        'teenagers_love': teenagers_love,
        'teenagers_bored': teenagers_bored,
        'request_teens': request_teens,
        'teenagers_enter2': teenagers_enter2
    }
    value = 'request_teens'
    if 'value' in event['state']['session']:
        value = event['state']['session']['value']
    return dict_funcs[value](event, context)