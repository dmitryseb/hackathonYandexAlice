import random
import pymorphy3
from advice_friendship import advices_fr
from advice_bored import advices_br

morph = pymorphy3.MorphAnalyzer()
end_text = "Было приятно пообщаться. Удачи тебе! Оставайся радостными человеком и приятным собеседником."

def have_sense(s, lists_of_key_words):
    lists_of_norm_forms = [[] for _ in range(len(lists_of_key_words))]
    for i in range(len(lists_of_key_words)):
        for w in lists_of_key_words[i]:
            lists_of_norm_forms[i] += [form.normal_form for form in morph.parse(w)]
    words = list(map(lambda s1: clear(s1), s.split()))
    input_norm_forms = []
    for w in words:
        input_norm_forms += [form.normal_form for form in morph.parse(w)]
    found = False
    res = -1
    for i in range(len(lists_of_norm_forms)):
        if found:
            break
        if len(set(input_norm_forms).intersection(set(lists_of_norm_forms[i]))) != 0:
            res = i
            found = True
            break
    return res

def clear(s):
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
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
    subtopics = ['Отношения с родителями', 'Школа', 'Друзья', 'Отношения', 'Эмоции']
    subtopic = ''
    value = 'request_teens'
    key_words = [['родители', 'мама', 'папа', 'отец', 'мать'],
                 ['школа'],
                 ['друг', 'дружба'],
                 ['отношения'],
                 ['эмоции', 'чувства']]
    res = have_sense(event['request']['original_utterance'], key_words)
    if res == -1:
        return request_teens(event, context, message='Выбери, пожалуйста, наиболее подходящую тему из списка.')
    else:
        subtopic = subtopics[res]
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
    key_words = [['друг', 'дружба', 'дружить'],
                 ['любовь', 'любить', 'отношения', 'парень', 'девушка', 'расставание', 'расстаться', 'бросить'],
                 ['скучно', 'скучать', 'скука', 'нечего', 'нечем']]
    res = have_sense(event['request']['original_utterance'], key_words)
    text = 'Извини, я пока не смогу поддержать разговор на эту тему. ' \
           'Вот примеры вопросов, с которыми я могу помочь: как найти друзей, как решить проблему в отношениях или что делать, если скучно.'
    value = 'teenagers_specify'
    buttons = []
    if res == 0:
        value = 'teenagers_friends'
        text = 'Поняла, тебя интересует, как найти друзей. ' \
               'Давай разберёмся, что такое дружба? Дружба – это регулярное общение и взаимопонимание. ' \
               'Старайся быть откровенным и честным, и ты обязательно найдёшь настоящих друзей. ' \
               'Хочешь, я дам тебе совет, как это сделать?'
    elif res == 1:
        value = 'teenagers_love'
        text = 'Поняла, ты хочешь поговорить об отношениях. Пожалуйста, выбери свой случай из списка.'
        buttons = [
            {'title': 'Мне нравится человек, а я ему нет'},
            {'title': 'Я нравлюсь человеку, а он мне нет'},
            {'title': 'У меня проблемы с моим партнёром'},
            {'title': 'Другой случай'},
        ]
    elif res == 2:
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
    if 'used_advices_fr' not in event['state']['session']:
        event['state']['session']['used_advices_fr'] = []
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
                'subtopic': event['state']['session']['subtopic'],
                'used_advices_fr': event['state']['session']['used_advices_fr']
            },
            'response': {
                'text': 'Извини, не поняла. Тебе нужен совет?',
                'end_session': 'false'
            },
        }
    used_advices_fr = event['state']['session']['used_advices_fr']
    if len(used_advices_fr) == len(advices_fr):
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Извини, советы закончились. " + end_text,
                'end_session': 'false'
            },
        }
    advice_id = random.randint(0, len(advices_fr) - 1)
    while advice_id in used_advices_fr:
        advice_id = random.randint(0, len(advices_fr) - 1)
    used_advices_fr.append(advice_id)
    text = advices_fr[advice_id] + '\nХочешь ещё один совет?'
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {
            'value': 'teenagers_friends',
            'subtopic': event['state']['session']['subtopic'],
            'used_advices_fr': used_advices_fr
        },
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }


def teenagers_love(event, context, message=''):
    response = clear(event['request']['original_utterance'])
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
    if response not in ['мне нравится человек а я ему нет', 'я нравлюсь человеку а он мне нет', 'у меня проблемы с моим партнёром']:
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
    if response == 'мне нравится человек а я ему нет':
        text = 'Не всегда мы можем понравиться другому человеку, и это нормально. Мы все разные и классные по-своему. Каждый из нас встретит того, кто ему подходит в правильное время. Если кто-то не оценил тебя так, как тебе бы хотелось, это не значит, что с тобой что-то не так. Просто ещё не пришло твоё время и не встретился твой человек.'
    elif response == 'я нравлюсь человеку а он мне нет':
        text = 'Не нужно чувствовать себя виноватым из-за этого. Не стоит начинать отношения из чувства жалости или вины. Ты не ответственен за чувства другого человека. Важно найти человека, с которым чувства будут взаимными. Взаимные чувства - это когда люди испытывают к нам ту же эмоцию, что и мы к ним. Бывает, что чувства не взаимны. Когда мы испытываем к людям одну эмоцию, а они к нам совсем другую. Это может быть печально, но жизнь такая.'
    elif response == 'у меня проблемы с моим партнёром':
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
    if 'used_advices_br' not in event['state']['session']:
        event['state']['session']['used_advices_br'] = []
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
                'value': 'teenagers_briends',
                'subtopic': event['state']['session']['subtopic'],
                'used_advices_br': event['state']['session']['used_advices_br']
            },
            'response': {
                'text': 'Извини, не поняла. Тебе нужна идея?',
                'end_session': 'false'
            },
        }
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
    text = advices_br[advice_id] + '\nХочешь ещё одну идею?'
    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {
            'value': 'teenagers_briends',
            'subtopic': event['state']['session']['subtopic'],
            'used_advices_br': used_advices_br
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