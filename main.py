import vk_api, sqlite3, requests, io, re
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import tok
from SQLighter import SQLighter
from parse import parser

vk_session = vk_api.VkApi(token = tok)
longpoll = VkBotLongPoll(vk_session, 203425909)



def sender(id, text):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0})


# инициализируем соединение с БД
db = SQLighter('ak_colladge.db')

ps = parser('Расписание')



for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            id = event.chat_id
            msg = event.object.message['text'].lower()
            
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

            patter = '[1-5][А-Яа-я][А-Яа-я][А-Яа-я]*\-[1-9]\-*[1-9]*'
            group = ''
            if type(re.match(patter, msg)) != type(None):
                group = (re.match(patter, msg).group(0)).lower()
            else:
                group = ''
            print(group)
            if dey == 'chat_invite_user':
                sender(id, f'Приветствую тебя, @id{invite_id}!')
            
            if msg == 'привет':
                sender(id, 'Приветствую!')
            elif msg == 'расписание':
                sender(id, ''.join(ps.parse(droup_for_db, 'Расписание')))
            elif msg == 'замена':
                sender(id, ''.join(ps.parse(droup_for_db, 'Замена')))
            elif msg == '/debug':
                sender(id, f'Отладочная информация: \n Основная: {db.get_chats(id)} \nГруппа в базе данных: {droup_for_db.upper()} \nСтатус соединения: {(requests.get(ps.URL)).status_code} \nВерсия бота: alpha 0.9')
            elif msg == '/start':
                if not db.chat_exists(id):
                    sender(id, 'Введите вашу группу в формате ЧXXX-Ч: ')
                else:
                    sender(id, 'Ваша группа уже добавлена в базу данных')
            
            elif msg == group:
                # если беседы нет в базе, добавляем его
                print('По маске:', re.match(patter, msg), ' без маски:', msg)
                db.add_chat(id, group)            
                sender(id, 'Ваша группа будет занесена в базу данных')
                #sender(id, 'Ваша группа введена не верно, повторите ввод по шаблону NXXX-N или NXX-N или NXXX-N-N, где N любое числа, а X любая буква')
            print('Сообщение: ', msg, ' Получили паттером: ', group)

            
