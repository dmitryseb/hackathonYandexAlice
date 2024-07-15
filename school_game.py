from useful_functions import create_response, remain_letters


def begin_type(event, context, message=""):
    answers = [remain_letters("Попрошу всех спокойно занять своё место.").lower().split(),
               remain_letters("Начну кричать на них, чтобы они перестали бегать.").lower().split(),
               remain_letters("Скажу, что поставлю всем двойки, если они не успокоятся.").lower().split(),
               remain_letters("Уйду из класса, дети сами проведут урок.").lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        if answers.index(event["request"]["nlu"]["tokens"]) == 3:
            text = "На выходе из школы тебя встречает директор. Он очень расстроен, что ты так безответственно относишься к своей обязанности учить детей, и увольняет тебя. \n"
            return konec(text, event, context, message)
        elif answers.index(event["request"]["nlu"]["tokens"]) > 0:
            text = 'Дети испуганно рассаживаются на место и затихают. Урок начинается. \n'
            return nach(text, event, context, message)
        text = 'Женя, Маша и Аня - прилежные ученики, поэтому они занимают своё место. А Антон и Илья - известные хулиганы, поэтому они продолжают бегать и шуметь. \n Твои действия:'
        buttons = [{"title": "Сделать им замечание строгим тоном."},
                   {"title": "Выгнать их из класса."}]
        return {
            "version": event["version"],
            "session": event["session"],
            "session_state": {"value": "chill_start"},
            "response": {
                "text": text,
                "end_session": "false",
                "buttons": buttons
            },
        }
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return begin_type(event, context, message)


def chill_start(event, context, message=""):
    answers = [remain_letters("Сделать им замечание строгим тоном.").lower().split(),
               remain_letters("Выгнать их из класса.").lower().split()]
    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        text = 'Антон и Илья начинают плакать и обещать, что они будут себя хорошо вести. Смягчившись, ты разрешаешь им остаться, и они занимают свои места. \n'
        if answers.index(event["request"]["nlu"]["tokens"]) == 0:
            text = 'Услышав строгий тон, Антон и Илья тоже успокаиваются и занимают свои места. \n'
        return nach(text, event, context, message)
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return chill_start(event, context, message)


def nach(text, event, context, message=""):
    text += 'Сегодня вы заканчиваете большую тему. Чему будет посвящён сегодняшний урок? \n'
    buttons = [{"title": "Проведу контрольную работу, чтобы проверить, как ученики усвоили материал."},
               {"title": "Сегодня ещё раз коротко повторим всю тему, а на следующем уроке будет контрольная."},
               {"title": "Проверю у учеников домашнее задание, чтобы узнать, всё ли им было понятно."}]
    return {
        "version": event["version"],
        "session": event["session"],
        "session_state": {"value": "urok"},
        "response": {
            "text": text,
            "end_session": "false",
            "buttons": buttons
        },
    }


def urok(event, context, message=""):
    answers = [
        remain_letters("Проведу контрольную работу, чтобы проверить, как ученики усвоили материал.").lower().split(),
        remain_letters(
            "Сегодня ещё раз коротко повторим всю тему, а на следующем уроке будет контрольная.").lower().split(),
        remain_letters("Проверю у учеников домашнее задание, чтобы узнать, всё ли им было понятно.").lower().split()]

    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        text = 'Дети начинают выполнять задания. На середине контрольной ты слышишь, как Маша спрашивает у Жени ответы. Как ты поступишь?'
        buttons = [{"title": "Сделаю вид, что ничего не было."},
                   {"title": "Скажу Маше, чтобы выполняла работу самостоятельно."}]
        val = "contra"
        if answers.index(event["request"]["nlu"]["tokens"]) == 1:
            text = 'Ты начинаешь объяснять материал, но скоро ты слышишь, как Аня громко разговаривает с Машей. Что будешь делать?'
            buttons = [{"title": "Продолжу объяснять несмотря на шум."},
                       {"title": "Сделаю замечание, чтобы они разговаривали тихо."}]
            val = "obyasn"
        elif answers.index(event["request"]["nlu"]["tokens"]) == 2:
            text = 'На вопрос, кто сделал домашнюю работу, руку поднимает только Женя. Ты знаешь, что у Ильи больше всех проблем с текущим материалом. Кого вызовешь к доске?'
            buttons = [{"title": "Женю"},
                       {"title": "Илью"}]
            val = "dz"

        return {
            "version": event["version"],
            "session": event["session"],
            "session_state": {"value": val},
            "response": {
                "text": text,
                "end_session": "false",
                "buttons": buttons
            },
        }
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return urok(event, context, message)


def contra(event, context, message=""):
    answers = [remain_letters("Сделаю вид, что ничего не было.").lower().split(),
               remain_letters("Скажу Маше, чтобы выполняла работу самостоятельно.").lower().split()]
    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        text = 'Все заканчивают и сдают работы. После проверки выясняется, что Женя и Маша написали контрольную хорошо, а остальные плохо. Теперь Маша будет думать, что она хорошо разбирается в данной теме, хотя на самом деле хорошо понял тему только Женя. Помни, что самостоятельные работы нужны в первую очередь для учеников, чтобы они знали, что им стоит изучить ещё раз! \n'
        if answers.index(event["request"]["nlu"]["tokens"]) == 1:
            text = 'Маша смущённо смотрит в свою работу. В конце урока все сдают работы, и после проверки выясняется, что тему хорошо усвоил только Женя. Теперь тебе легче будет спланировать следующие уроки, чтобы все ученики разобрались в теме. \n'
        return konec(text, event, context, message)
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return chill_start(event, context, message)


def obyasn(event, context, message=""):
    answers = [remain_letters("Продолжу объяснять несмотря на шум.").lower().split(),
               remain_letters("Сделаю замечание, чтобы они разговаривали тихо.").lower().split()]
    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        text = 'На следующем уроке все пишут контрольную, и результаты у всех плохие. Из-за шума никто не смог понять объяснений на прошлом уроке. Тишина во время занятий помогает и учителям и ученикам! \n'
        if answers.index(event["request"]["nlu"]["tokens"]) == 1:
            text = 'На следующем уроке все пишут контрольную, и у всех хорошие результаты! Директор поздравляет тебя с тем, что все ученики так хорошо освоили трудную тему, и выдаёт премию. Отличная работа! \n'
        return konec(text, event, context, message)
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return chill_start(event, context, message)


def dz(event, context, message=""):
    answers = [remain_letters("Женю.").lower().split(),
               remain_letters("Илью.").lower().split()]
    if "request" in event and "nlu" in event["request"] and "tokens" in event["request"]["nlu"] and \
            event["request"]["nlu"]["tokens"] in answers:
        text = 'Женя выходит к доске и всё отвечает правильно. На следующем уроке дети пишут контрольную, и все кроме Жени пишут плохо. Помни, что всегда кто-то усваивает новые знания быстрее, кто-то медленнее, а учитель должен помогать и тем, и тем. \n'
        if answers.index(event["request"]["nlu"]["tokens"]) == 1:
            text = 'Илья выходит к доске, и ты вместе с классом помогаешь ему разобраться в домашнем задании. На следующем уроке все пишут контрольную, и у всех отличные результаты! Директор поздравляет тебя с тем, что все ученики так хорошо освоили трудную тему и выдаёт премию. Отличная работа! \n'
        return konec(text, event, context, message)
    message = "Некорректный ответ. Пожалуйста, выбери другой вариант ответа"
    return chill_start(event, context, message)


def konec(text, event, context, message=""):
    message = text + 'Наша игра закончена. Теперь ты больше знаешь о том, что чувствуют учителя, когда ведут у тебя уроки. Это очень непростая работа, поэтому старайся вести себя хорошо!'
    return create_response(event, {"value": "show_topics"}, text=message)


def school_game(event, context, message=""):
    text = 'Предлагаю тебе взглянуть на школу по-новому. Представь, что ты школьный учитель, которому предстоит сейчас провести урок. ' \
           'Ты заходишь в класс и видишь своих учеников: Илью, Антона, Женю, Аню и Машу. Звонок уже прозвенел, но дети всё ещё носятся по классу. \n' \
           'Как ты начнёшь урок?'
    buttons = [{"title": "Попрошу всех спокойно занять своё место."},
               {"title": "Начну кричать на них, чтобы они перестали бегать."},
               {"title": "Скажу, что поставлю всем двойки, если они не успокоятся"},
               {"title": "Уйду из класса, дети сами проведут урок."}]

    return {
        "version": event["version"],
        "session": event["session"],
        "session_state": {"value": "begin_type"},
        "response": {
            "text": text,
            "end_session": "false",
            "buttons": buttons
        },
    }
