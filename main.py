import vk_api, sqlite3, requests, io
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
                ps.parse('Расписание')
            elif msg == '/debug':
                sender(id, f'Отладочная информация: {db.get_chats(id)}')
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
                

            
