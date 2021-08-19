import vk_api, sqlite3, requests, io, string
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
            
            if dey == 'chat_invite_user':
                sender(id, f'Приветствую тебя, @id{invite_id}!')
            
            if msg == 'привет':
                sender(id, 'Приветствую!')
            elif msg == 'расписание':
                sender(id, ''.join(ps.parse('Расписание')))
            elif msg == 'замена':
                sender(id, ''.join(ps.parse('Замена')))
            elif msg == '/debug':
                
                #чистим инфу от лишних симоволов (string.punctuation) (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~)
                droup_for_db = " ".join(str(x) for x in db.get_group(id))
                for p in string.punctuation:
                    if p in droup_for_db:
                        # банальная замена символа в строке
                        droup_for_db = droup_for_db.replace(p, '')

                sender(id, f'Отладочная информация: \n Основная: {db.get_chats(id)} \nГруппа в базе данных: {droup_for_db.upper()} \nСтатус соединения: {(requests.get(ps.URL)).status_code}')
            elif msg == '/start':
                sender(id, 'Введите вашу группу в формате ЧXXX-Ч: ')
                for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        if(not db.chat_exists(id)):
                            # если беседы нет в базе, добавляем его
                            msgGroup = event.object.message['text'].lower()
                            db.add_chat(id, msgGroup)            
                            sender(id, 'Ваша группа будет занесена в базу данных')
                            break
                        else:
                            sender(id, 'Ваша группа уже добавлена в базу данных')
                            break
                

            
