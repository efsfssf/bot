from docx import Document
from dateutil import parser
import os, locale, re

filename = 'Замена_на_14_декабря_2019_г..docx'
wordDoc = Document(os.getcwd() + f"\\{filename}")
#заменяем название в файле:
if filename.find('января') != -1:
    filename = filename.replace('января', 'January')
elif filename.find('февраля') != -1:
    filename = filename.replace('февраля', 'February')
elif filename.find('марта') != -1:
    filename = filename.replace('марта', 'March')
elif filename.find('апреля') != -1:
    filename = filename.replace('апреля', 'April')
elif filename.find('мая') != -1:
    filename = filename.replace('мая', 'May')
elif filename.find('июня') != -1:
    filename = filename.replace('июня', 'June')
elif filename.find('июля') != -1:
    filename = filename.replace('июля', 'July')
elif filename.find('августа') != -1:
    filename = filename.replace('августа', 'August')
elif filename.find('сентября') != -1:
    filename = filename.replace('сентября', 'September')
elif filename.find('октября') != -1:
    filename = filename.replace('октября', 'October')
elif filename.find('ноября') != -1:
    filename = filename.replace('ноября', 'November')
elif filename.find('декабря') != -1:
    filename = filename.replace('декабря', 'December')

weekday_list = {"Понедельник":1,"Вторник":2,"Среда":3,"Четверг":4,"Пятница":5,"Суббота":6,"Воскресенье":7}
weekday_list1 = {value:key for key, value in weekday_list.items()}

#получаем на какой день недели расписание
locale.setlocale(locale.LC_TIME, 'ru')
extr_date = re.search("(\d+.+?)_г", filename).group(1).replace("_"," ")
week_day = parser.parse(extr_date).weekday()+1

#получаем день недели в виде букв
liva_weekday = weekday_list1.get(week_day)
print('Будет показано расписание на: ', liva_weekday)

for table in wordDoc.tables:
    for row in table.rows:
        if '3исп-9'.upper() in row.cells[0].text:
            print(row.cells[0].text)
