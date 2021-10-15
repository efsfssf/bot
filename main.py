# coding=utf-8
import vk_api, requests, re, time, json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from config import tok, bot_id
from SQLighter import SQLighter
from parse import parser
from vktools import Carousel, Element, Text, ButtonColor

# VK
vk_session = vk_api.VkApi(token = tok)

longpoll = VkBotLongPoll(vk_session, bot_id)

CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')

def get_but(text, color):
    return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }
 
keyboard1 = {
    "one_time" : False,
    "buttons" : [
        [get_but('Опаздаю', 'secondary'), get_but('Расписание', 'primary')],
        [get_but('/help', 'secondary')]
    ]
}
keyboard1 = json.dumps(keyboard1, ensure_ascii = False).encode('utf-8')
keyboard1 = str(keyboard1.decode('utf-8'))


def sender(id, text, keyboard=keyboard1, template=None):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'keyboard' : keyboard, 'template' : template, 'random_id' : 0})

def sender_CallBack(event_id, user_id, peer_id, event_data):
    vk_session.method('messages.sendMessageEventAnswer', {'event_id' : event_id, 'user_id' : user_id, 'peer_id' : peer_id, 'event_data' : event_data})


# инициализируем соединение с БД | VK
db = SQLighter('ak_colladge.db')

ps = parser('Расписание')


print("VK")
# VK
while True:
    try:
        f_toggle: bool = False
        for event in longpoll.listen():
            print("EVENT VK")
            if event.type == VkBotEventType.MESSAGE_NEW:
                print("MESSADGE VK")
                msg = event.object.message['text'].lower()
                if event.from_chat:
                    id = event.chat_id

                    try:
                        dey = event.message.action['type']
                        invite_id = event.message.action['member_id']
                    except:
                        dey = ''
                        invite_id = -100

                    #чистим инфу от лишних симоволов
                    punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
                    droup_for_db = " ".join(str(x) for x in db.get_group(id))
                    for p in punctuation:
                        if p in droup_for_db:
                            # банальная замена символа в строке
                            droup_for_db = droup_for_db.replace(p, '')
                            droup_for_db = droup_for_db.replace(' ', '')

                    print('\n\n\n**********\n\n\nГруппа:', str(droup_for_db))

                    f1 = open("text1.txt", 'w', encoding="utf-8")
                    f1.write(droup_for_db)
                    f1.close()

                    patter = '[1-5][А-Яа-я][А-Яа-я][А-Яа-я]*\-[1-9]\-*[1-9]*'
                    group = ''
                    if type(re.match(patter, msg)) != type(None):
                        group = (re.match(patter, msg).group(0)).lower()
                    else:
                        group = ''
                    
                    if dey == 'chat_invite_user':
                        sender(id, f'Приветствую тебя, @id{invite_id}!')
                    
                    if '@agent' in msg:
                        msg = msg.partition(' ')[2]
                    print('Сообщение: ', msg)
                    if msg == 'расписание':
                        #content = ''.join(ps.parse(droup_for_db, 'Замена', False, True))
                        #if content == "Замен нет": content = "Увы, замен нет"
                        #else: content = "Есть замены" 
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_button("Следующий день")
                        #keyboard.add_callback_button(label='Есть ли замены', payload={"type": "show_snackbar", "text": content})
                        sender(id, ''.join(ps.parse('4исп-9', 'Расписание', False, True, 'нет')), keyboard=keyboard.get_keyboard())
                    elif msg == 'расписание -замена':
                        sender(id, ''.join(ps.parse(droup_for_db, 'Расписание', False, False, 'нет')))
                    elif msg == 'следующий день':
                        sender(id, ''.join(ps.parse(str(droup_for_db), 'Расписание', True, False, 'нет')))
                        sender(id, 'Без учёта возможных замен')
                    elif msg == 'замена':
                        content = ''.join(ps.parse(droup_for_db, 'Замена', False, False))
                        sender(id, content)
                    elif msg == '/debug':
                        sender(id, f'Отладочная информация: \n\n Основная: {db.get_chats(id)} \nГруппа в базе данных: {droup_for_db.upper()} \nСтатус соединения: {(requests.get(ps.URL)).status_code} \nСписок домашних заданий: \nweather connect status: \nВерсия бота: beta 0.11.2.0')
                    elif msg == '/help' or msg == '/list':
                        content = f'&#128210;Список команд: \n*********************\n\n Расписание -замена — расписание без замен \n Расписание+ — расписание на любой день недели \nЗвонки — показывает список звонков \nЗвонки Завтра — показывает список звонков на следующий день \nПеремены — показывает список перемен \nСкачать AST — бот даст ссылку на AST-Test \nПароли AST — Скоро \nСкачать 1C — бот даст ссылку на 1C'
                        sender(id, content)
                    elif msg == 'скачать 1c':
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_callback_button(label='Скачать', payload={"type": "open_link", "link": "https://turb.to/2630vu4bnwiy/8.3.16.1296_Windows_RePack_x64.rar.html"})
                        sender(id, '1С:Предприятие \nВерсия: 8.3.16.1296 RePack \nТип установки: простая установка x64 \nРазмер:425 МБ', keyboard=keyboard.get_keyboard())
                    elif msg == 'звонки':
                        content = '08:00 - 09:30 \n09:40 - 11:10 \n11:30 - 13:00 \n13:10 - 14:40 \n15:00 - 16:30 \n16:40 - 18:10 \n18:20 - 19:50'
                        sender(id, content)
                    elif msg == 'скачать ast':
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_callback_button(label='Скачать', payload={"type": "open_link", "link": "http://lk.volbi.ru/files/documenti/setup_AST-Test_Player_4.3.7.2.exe"})
                        sender(id, 'AST-Test Player \nВерсия: 4.3.7.2 \nС сайта АНПОО "Академический колледж" \nРазмер:10.1 МБ', keyboard=keyboard.get_keyboard())
                    elif msg == 'перемены':
                        content = '09:30 - 09:40  \n11:10 - 11:30 \n13:00 - 13:10\n14:40 - 15:00\n16:30 - 16:40\n18:10 - 18:20'
                        sender(id, content)
                    elif msg == '/test':
                        #content = ''.join(ps.parse(droup_for_db, 'Замена', False, False))
                        sender(id, content)
                    elif msg == 'пн' or msg == 'вт' or msg == 'ср' or msg == 'чт' or msg == 'пт' or msg == 'сб' or msg == 'вс':
                        if msg == 'вс':
                            sender(id, 'дурачёк?')
                        else:
                            sender(id, ''.join(ps.parse(droup_for_db, 'Расписание', False, False, msg)))
                    elif msg == "полное расписание" or msg == "расписание+":

                        carousel = {
                            "type": "carousel",
                            "elements": [{
                                    "photo_id": "-206674494_457239035",
                                    "title": "Понедельник",
                                    "description": "Показать расписание на понедельник",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "пн",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239034",
                                    "title": "Вторник",
                                    "description": "Показать расписание на вторник",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "вт",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239037",
                                    "title": "Среда",
                                    "description": "Показать расписание на среду",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "ср",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239039",
                                    "title": "Четверг",
                                    "description": "Показать расписание на четверг",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "чт",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239036",
                                    "title": "Пятница",
                                    "description": "Показать расписание на пятницу",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "пт",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239038",
                                    "title": "Суббота",
                                    "description": "Показать расписание на субботу",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "сб",
                                            "payload": "{}"
                                        }
                                    }]
                                }
                            ]
                        }
                        carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
                        carousel = str(carousel.decode('utf-8'))

                        sender(id, 'Выберите день недели: ', keyboard=None, template=carousel)
                    elif msg == '/start':
                        if not db.chat_exists(id):
                            sender(id, 'Введите вашу группу в формате ЧXXX-Ч: ')
                        else:
                            sender(id, 'Ваша группа уже добавлена в базу данных')

                    elif type(msg) != type(None) and msg != "" and msg == group:
                        # если беседы нет в базе, добавляем его
                        print('По маске:', re.match(patter, msg), ' без маски:', msg)
                        db.add_chat(id, group)
                        sender(id, 'Ваша группа будет занесена в базу данных')
                        #sender(id, 'Ваша группа введена не верно, повторите ввод по шаблону NXXX-N или NXX-N или NXXX-N-N, где N любое числа, а X любая буква')
                    print('Сообщение: ', msg, ' Получили паттером: ', group)
            # обрабатываем клики по callback кнопкам
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                # если это одно из 3х встроенных действий:
                if event.object.payload.get('type') in CALLBACK_TYPES:
                    sender_CallBack(event.object.event_id, event.object.user_id, event.object.peer_id, json.dumps(event.object.payload))
            
            
    except requests.exceptions.Timeout:
        time.sleep(60)
        pass

