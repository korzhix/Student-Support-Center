from fuzzywuzzy import fuzz
from vk_api.utils import get_random_id
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Здесь токен, который нужно взять в настройках группы
token = 'token'

#библиотека ключевых слов и команд
opts = {
    "tbr": ('скажи', 'расскажи', 'покажи', 'какая', 'как', 'кто', 'сколько'
            'какой', 'какое', 'какую', 'имеет', 'студент', 'какие'),
    "cmds": {
        "stipendia": ('стипендия', 'стипендия в 1 семестре', 'степуха', 'выплачивают стипендии', 'получает стипендии'),
        "web": ('сайт юфу', 'сайт'),
        "bank": ('банковская карточка', 'банковская карточка стипендия',
                 'выплачивает стипендию'),
        "fizra": ('поменять препода по физре', 'сменить преподавателя по физре',
                  'перезаписаться на физическую культуру'),
        "nikita": ('пидор', 'пидорас')
    }
}

#основная функция, вызывающая другие функции
def cmdback(question):
    cmd = question

    # Вырезаем вспомогательные слова
    for x in opts['tbr']:
        cmd = cmd.replace(x, "").strip()

    # Распознавание и исполнение
    cmd = recognize_cmd(cmd)
    msg = execute_cmd(cmd['cmd'])
    return msg


def recognize_cmd(cmd):
    # Распознавание команды
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    if RC['percent'] < 40:
        RC['cmd'] = 'dontknow'

    return RC


def execute_cmd(cmd):
    #Исполнение команды

    if cmd == 'stipendia':
        # сказать размер стипендии
        msg = 'Базовая стипендия - 2000 рублей в месяц'

    elif cmd == 'web':
        # сказать сайт юфу
        msg = 'https://sfedu.ru'

    elif cmd == 'bank':
        # сказать банк который выплачивает стипендию
        msg = 'Банк Центр-Инвест'

    elif cmd == 'fizra':
        msg = '''Демьянова Людмила Михайловна - зав.кафедрой, любые манипуляции
с записью и перезаписью осуществляет она'''

    elif cmd == 'nikita':
        msg = 'Я уверен, что пидорас - Никита Назаренко с 3 группы 1 курса'

    else:
        msg = 'На такой вопрос мы не можем ответить'
    return msg

# Запуск программы
vk_session = vk_api.VkApi(token=token)

vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        response = event.text.lower()

        msg = cmdback(response)

        vk.messages.send(
            random_id = get_random_id(),
            user_id = event.user_id,
            message = msg
        )
