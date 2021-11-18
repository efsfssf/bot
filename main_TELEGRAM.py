from sys import version
import telebot, re, requests
from telebot import types
from SQLighter_TELEGRAM import SQLighter_TELEGRAM
from config import token_telegram
from parse import parser
import os
import sys

#версия бота (для обноваления)
version_current = '0.11.1.0'

# инициализируем соединение с БД | TELEGRAM
db_TELEGRAM = SQLighter_TELEGRAM('ak_colladge_TELEGRAM.db')

ps = parser('Расписание')

# TELEGRAM
bot = telebot.TeleBot(token_telegram)


@bot.message_handler(commands=['start'])
def welcome(message):
    #keyboard standart
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/Опоздаю")
    item2 = types.KeyboardButton("/Расписание")

    markup.add(item1, item2)

    #keyboard inline
    markup_Inline = types.InlineKeyboardMarkup(row_width=3)
    item1_1_Inline = types.InlineKeyboardButton("3ИСП-9-1", callback_data='3ISP-9-1')
    item1_Inline = types.InlineKeyboardButton("3ИСП-9-2", callback_data='3ISP-9-2')
    item2_Inline = types.InlineKeyboardButton("4ИСП-9", callback_data='4ISP-9')
    item3_Inline = types.InlineKeyboardButton("4ПД-9", callback_data='4PD-9')
    item4_Inline = types.InlineKeyboardButton("4ГД-9", callback_data='4GD-9')
    item5_Inline = types.InlineKeyboardButton("3ТОП-9", callback_data='3TOP-9')
    item6_Inline = types.InlineKeyboardButton("3БД-9", callback_data='3BD-9')
    item7_Inline = types.InlineKeyboardButton("3Б-9", callback_data='3B-9')
    item8_Inline = types.InlineKeyboardButton("3ЗИО-9", callback_data='3ZIO-9')
    item9_Inline = types.InlineKeyboardButton("3К-9", callback_data='3K-9')
    item10_Inline = types.InlineKeyboardButton("3ПД-9-1", callback_data='3PD-9-1')
    item11_Inline = types.InlineKeyboardButton("3ПД-9-2", callback_data='3PD-9-2')
    item12_Inline = types.InlineKeyboardButton("3ПСО-9", callback_data='3PSO-9')
    item13_Inline = types.InlineKeyboardButton("2ТОП-9", callback_data='2TOP-9')
    item14_Inline = types.InlineKeyboardButton("2ИСП-9-1", callback_data='2ISP-9-1')

    markup_Inline.add(item1_1_Inline, item1_Inline, item2_Inline, item3_Inline, item4_Inline, item5_Inline, item6_Inline, item7_Inline, item8_Inline, item9_Inline, item10_Inline, item11_Inline,
    item12_Inline, item13_Inline, item14_Inline)
    
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1_1 = types.KeyboardButton("/Следующий день")
    item2_2 = types.KeyboardButton("/Расписание")
    markup1.add(item1_1, item2_2)


    bot.send_message(message.chat.id, 'Спасибо, что выбрал нашего бота!☺️ Введите вашу группу в формате ЧXXX-Ч или выберите: ', reply_markup= (markup if message.chat.type == 'group' else markup1))
    bot.send_message(message.chat.id, '3-4 курсы: ', reply_markup=markup_Inline)


@bot.message_handler(content_types=['text'])
def main(message):
    
    #чистим инфу от лишних симоволов
    punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    droup_for_db = " ".join(str(x) for x in db_TELEGRAM.get_group(message.chat.id))
    for p in punctuation:
        if p in droup_for_db:
            # банальная замена символа в строке
            droup_for_db = droup_for_db.replace(p, '')
            droup_for_db = droup_for_db.replace(' ', '')

    print('\n\n\n**********\n\n\nГруппа:', str(droup_for_db))

    f1 = open("text2.txt", 'w', encoding="utf-8")
    f1.write(droup_for_db)
    f1.close()

    patter = '[1-5][А-Яа-я][А-Яа-я][А-Яа-я]*\-[1-9]\-*[1-9]*'
    group = ''
    if type(re.match(patter, str(message.text))) != type(None):
        group = (re.match(patter, message.text).group(0)).lower()
    else:
        group = ''

    if message.chat.type == 'private' or message.chat.type == 'group':
        if (message.text).lower() == '/расписание' or message.text == '/schedule' or message.text == '/schedule@agent11bot':
            bot.send_message(message.chat.id, (''.join(ps.parse(str(droup_for_db), 'Расписание', False, True, 'нет'))).replace('&#128341;', '🕙').replace('&#128260;', '🔄'))
        elif (message.text).lower() == '/debug' or message.text == '/debug@agent11bot':
            bot.send_message(message.chat.id, f'Отладочная информация: \n\n Основная: {db_TELEGRAM.get_chats(message.chat.id)} \nГруппа в базе данных: {droup_for_db.upper()} \nСтатус соединения: {(requests.get(ps.URL)).status_code} \nСписок домашних заданий: \nweather connect status: \nВерсия бота: beta {version_current} \n\nОсновано на Аген №11 VK BOT create by Alexey Orlov')
        elif (message.text).lower() == '/следующий день' or message.text == '/следующий день@agent11bot':
            bot.send_message(message.chat.id, (''.join(ps.parse(str(droup_for_db), 'Расписание', True, False, 'нет'))).replace('&#128341;', '🕙'))
            bot.send_message(message.chat.id, 'Без учёта возможных замен')
        elif (message.text).lower() == '/update':
            f = open('version.txt', encoding="utf-8")
            version_server = f.read()
            if version_current != version_server:
                bot.send_message(message.chat.id, f'Текущая версия {version_current}. Версия на сервере {version_server} \nОбновление...')
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                bot.send_message(message.chat.id, f'Версия на сервере совпадает с текущей версией \nТекущая версия {version_current}. Версия на сервере {version_server}', )
        elif (message.text).lower() == '/clear':
            bot.send_message(message.chat.id, 'Клавиатура удалена', reply_markup= types.ReplyKeyboardRemove())
        elif type(message.text) != type(None) and (message.text).lower() != "" and (message.text).lower() == group:
            # если беседы нет в базе, добавляем его
            print('По маске:', re.match(patter, message.text), ' без маски:', message.text)
            add_chat_TELEGRAM(message.chat.id, group)
            #bot.send_message(id_chat, 'Ваша группа уже добавлена в базу данных')
            #sender(message.chat.id, 'Ваша группа введена не верно, повторите ввод по шаблону NXXX-N или NXX-N или NXXX-N-N, где N любое числа, а X любая буква')
        print('Сообщение: ', (message.text).lower(), ' Получили паттером: ', group)
    

#callback Inline
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            #ref
            if call.data == '3ISP-9-1':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3ИСП-9-1')
                add_chat_TELEGRAM(call.message.chat.id, '3ИСП-9-1')
            if call.data == '3ISP-9-2':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3ISP-9-2')
                add_chat_TELEGRAM(call.message.chat.id, '3ИСП-9-2')
            elif call.data == '4ISP-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 4ИСП-9')
                add_chat_TELEGRAM(call.message.chat.id, '4ИСП-9')
            elif call.data == '4PD-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 4ПД-9')
                add_chat_TELEGRAM(call.message.chat.id, '4ПД-9')
            elif call.data == '4GD-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 4ГД-9')
                add_chat_TELEGRAM(call.message.chat.id, '4ГД-9')
            elif call.data == '3TOP-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3TOP-9')
                add_chat_TELEGRAM(call.message.chat.id, '3TOP-9')
            elif call.data == '3BD-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3БД-9')
                add_chat_TELEGRAM(call.message.chat.id, '3БД-9')
            elif call.data == '3B-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3Б-9')
                add_chat_TELEGRAM(call.message.chat.id, '3Б-9')
            elif call.data == '3ZIO-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3ЗИО-9')
                add_chat_TELEGRAM(call.message.chat.id, '3ЗИО-9')
            elif call.data == '3K-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3К-9')
                add_chat_TELEGRAM(call.message.chat.id, '3К-9')
            elif call.data == '3PD-9-1':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3ПД-9-1')
                add_chat_TELEGRAM(call.message.chat.id, '3ПД-9-1')
            elif call.data == '3PD-9-2':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3ПД-9-2')
                add_chat_TELEGRAM(call.message.chat.id, '3ПД-9-2')
            elif call.data == '3PSO-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 3ПСО-9')
                add_chat_TELEGRAM(call.message.chat.id, '3ПСО-9')
            elif call.data == '2TOP-9':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 2TOP-9')
                add_chat_TELEGRAM(call.message.chat.id, '2TOP-9')
            elif call.data == '2ISP-9-1':
                bot.send_message(call.message.chat.id, 'Выбрана группа: 2ИСП-9-1')
                add_chat_TELEGRAM(call.message.chat.id, '2ИСП-9-1')
            

            #remove
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='[Антиспам] Это временное сообщение больше не имеет смысла. Оно было удалено', reply_markup=None)

            #show notif 
            #NEED FIX!!!!
            #bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text='Сохранено в базе данных')

    except Exception as e:
        print(repr(e))

def add_chat_TELEGRAM(id_chat, group):
    # если беседы нет в базе, добавляем его
    if not db_TELEGRAM.chat_exists(id_chat):
        db_TELEGRAM.add_chat(id_chat, group)
    else:
        bot.send_message(id_chat, 'Ваша группа уже добавлена в базу данных')


#run
bot.infinity_polling(timeout=10, long_polling_timeout = 5)