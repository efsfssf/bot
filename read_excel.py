import openpyxl, os, datetime, re
import win32com.client as win32
import numpy as np
import itertools
from itertools import groupby
from collections import Counter

if not os.path.exists('Расписание_1-4_курсов_с_01.04_по_05.07.2021_(2_поток).xlsx'):   #если этого файла нет, создаем новый
    fname = (os.getcwd() + "\\Расписание_1-4_курсов_с_01.04_по_05.07.2021_(2_поток).xls").replace('\\', '\\') #ищем файл со старым расширением
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fname)
    wb.SaveAs(fname+"x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension              сохраняем в новом формате
    wb.Close()                               #FileFormat = 56 is for .xls extension
    excel.Application.Quit()


# чекаем файл
wb = openpyxl.reader.excel.load_workbook(filename="Расписание_1-4_курсов_с_01.04_по_05.07.2021_(2_поток).xlsx")
wb.active = 0

sheet = wb.active




weekday_list = {"Понедельник":1,"Вторник":2,"Среда":3,"Четверг":4,"Пятница":5,"Суббота":6,"Воскресенье":7}
weekday_list1 = {value:key for key, value in weekday_list.items()}

#a_dict = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8, "I":9, "J":10, "K":11, "L":12, "M":13, "N":14, "O":15, "P":16, "Q":17, "R":18, "S":19, "T":20, "U":21, "V":22, "W":23, "X":24, "Y":25}
a_dict = list(map(chr, range(97,123))) #для поиска группы по столбцам
a = range(4, 7) #для поиска группы по строкам
weekday_range = range(4, 100) #для поиска дня недели
length_list = (3, 5) # сколько может быть пар в один день  с учетом пустых ячеек

# получаем день недели
#liva_weekday = weekday_list1.get(datetime.datetime.today().isoweekday())
liva_weekday = input('Введите день недели:')
if liva_weekday == 'Воскресенье':
    liva_weekday = 'Понедельник'
    
weekly_schedule = []
for number in a: #цифры/строки
    for key in a_dict: #буквы/столбцы
        if type(sheet[key + str(number)].value) != type(None): #если ячейка не пустая
            if '3исп-9'.upper() in sheet[key + str(number)].value: #ищем группу в расписании
                
                #пробегаем в цикле по ячейки для поиска дня недели
                for day in weekday_list: # пробигаемся по дням неделям
                    if day == liva_weekday: # если мы нашли день недели равным текущему
                        for number_day in weekday_range: # пробигаемся по определенном диапозоне для поиска ...
                            if type(sheet[key + str(number_day)].value) != type(None): #если ячейка не пустая
                                if day in sheet[key + str(number_day)].value: #Нашли день недели
                                    next_day = weekday_list.get(day)+1 # поменчаем, что неделя следующая (если сейчас 5, то парсим до 6)
                                    lest_day_text = weekday_list1.get(next_day)# ищем номер недели в списке (чтобы писалась неделя текстом, а не цифрой)
                                    
                                    next_weekday_range = range(number_day, 100) # Диапозон от сегодняшнего дня недели до не найденного следующего (будем искать от сегодняшней до 100 ячейки)
                                    
                                    for day_next in weekday_list:
                                        if day_next == lest_day_text:
                                            for number_day_next in next_weekday_range: #пробегаем в цикле по ячейки для поиска след дня недели
                                                if type(sheet[key + str(number_day_next)].value) != type(None): #если ячейка не пустая
                                                    if day_next in sheet[key + str(number_day_next)].value: #Нашли завтрашний день недели
                                                        
                                                        list_object = range(number_day+1, number_day_next) #от сегодняшнего дня недели до завтрашнего
                                                        name = []
                                                        time = []
                                                        for obj in list_object:
                                                            if type(sheet[key + str(obj)].value) != type(None):
                                                                
                                                                #ФАМИЛИИ | NAME
                                                                s = sheet[key + str(obj)].value # найденные ячейки с парами
                                                                patter = r'[А-ЯЁа-яё]+\s[А-ЯЁа-яё]{1}\.\s*[А-ЯЁа-яё]{1}\.\s*\/*\s*[А-ЯЁа-яё]*\s*[А-ЯЁа-яё]*\.*\s*[А-ЯЁа-яё]*\.*' # ищем фамилии
                                                                name.append(re.findall(patter, s)) # заносим найденные фамилии в ячейках s в список name

                                                                #ВРЕМЯ | TIME
                                                                patterTIME = r'[0-9][0-9]\:[0-9][0-9][ \t]*\-*\—*[ \t]*[0-9][0-9]\:[0-9][0-9]\,*[0-9]*[0-9]*\:*[0-9]*[0-9]*[ \t]*\-*\—*[ \t]*[0-9]*[0-9]*\:*[0-9]*[0-9]*[ \t]*\-*\—*[ \t]*[0-9]*[0-9]*\:*[0-9]*[0-9]*'
                                                                time.append(re.findall(patterTIME, s))
                                                                
                                                                #ЗАПОЛНЯЕМ СПИСОК РАСПИСАНИЕМ | weekly_schedule
                                                                weekly_schedule.append(s) # заполянем список парами
                                                        
                                                        #ФОРМАТИРУМ МАТРИЦУ С ФАМИЛИЯМИ
                                                        name = ([x for x in name if x])
                                                        name = [el for el, _ in groupby(name)]
                                                        name = sum(name, [])

                                                        name = [line.rstrip() for line in name] #удаляем символы \n из строки времени

                                                        print('NAME:', name)

                                                        #ФОРМАТИРУМ МАТРИЦУ С ВРЕМЕНЕМ
                                                        time = ([x for x in time if x])
                                                        time = [el for el, _ in groupby(time)]
                                                        time = sum(time, [])

                                                        time = [line.rstrip() for line in time] #удаляем символы \n из строки времени

                                                        print('TIME:', time, 'Пара начинается в', time[0][:5], 'Домой в', time[-1][-5:])
                                                        
                                                        result = [w for w in weekly_schedule if w not in name]
                                                        
                                                        """
                                                        time_current = []
                                                        for i, (start, end) in enumerate(zip(time[::2], time[1::2]), 1):
                                                            time_current.append(f"{start} - {end}")
                                                             #   if re.search(patterTIME, s) is not None:
                                                       
                                                        print(time_current)
                                                        """
                                                        
                                                        pTIME = r'[0-9][0-9]\:[0-9][0-9]'
                                                        
                                                        count = 0
                                                        for item_i in range(len(result)):
                                                            if re.search(pTIME, result[item_i]) is not None:
                                                                patterTIME_del = r'[0-9][0-9]\:[0-9][0-9][ \t]*\-*\—*[ \t]*[0-9][0-9]\:[0-9][0-9]\,*[0-9]*[0-9]*\:*[0-9]*[0-9]*[ \t]*\-*\—*[ \t]*[0-9]*[0-9]*\:*[0-9]*[0-9]*[ \t]*\-*\—*[ \t]*[0-9]*[0-9]*\:*[0-9]*[0-9]*'
                                                                result[item_i] = re.sub(patterTIME_del, '', result[item_i]) # удаляем лишнее время из списка (то, что без скобок)
                                                                
                                                                #print('COUNT:', count, ' item_i:', item_i)
                                                                result[item_i] += '  (' + time[count] + ')' #добавляем скобки
                                                                count += 1
                                                        
                                                        result = [line.rstrip() for line in result] #удаляем символы \n из строки результата
                                                        print('\nРЕЗУЛЬТАТ:', result)
                                                        
                                                        
                                                        
                                                        
                                                        


                                                  
#print(weekly_schedule) # выводим результат


