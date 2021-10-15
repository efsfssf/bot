# coding=utf-8
import requests, re, os, json
from bs4 import BeautifulSoup
import read_excel, read_word, merge

class parser:
    URL = 'http://academicol.ru/students/schedule/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    HOST = 'http://academicol.ru/'

    def __init__(self, text):
        self.text = text

    def get_html(self, url, params=None):
        r = requests.get(url, headers=self.HEADERS, params=params)
        return r

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('table' ,attrs={'class':'table_normativnaja_dokumentacija'}).find_all('td', {'class': 'tdschedule', 'bgcolor': ['#FFFFFF', '#F2F2F2']})

        schedule = []
        for item in items:
            sc = item
            if item.get_text():
                if type(item.find('a', {'id': 'black'})) != type(None):
                    scLink = 'http://academicol.ru/' + item.find('a', {'id': 'black'}).get('href')
                    scName = item.find('a', {'id': 'black'}).get_text()
                else:
                    continue

            else:
                continue
            schedule.append({
                'title': scName,
                'link': scLink,
            })

        return schedule

    
    file_name_list = []
    
    def file_search(self, group, schedule, text, next_day, mergeStatus, weekday_parse):
        test_file_name_list = ['Замена_на_31_августа_2021_г..docx', 'Расписание_1_2_курсов_с_01_04_по_05_07_2021_1_поток', 'Расписание_1-4_курсов_с_01.04_по_05.07.2021_(2_поток)']
        
        if not self.file_name_list:
            return 'Расписания нет'
        print('Список файлов:', self.file_name_list)

        """
        if not 'Замена' in self.file_name_list:
            print("Замен нет")
            mergeStatus = False
        """
        schedule_main = ''
        if mergeStatus == False:
            for j in self.file_name_list:
                if text == 'Расписание' and text in j:
                    print('\nОткрытие файла:', j)
                    schedule = read_excel.main_open(group, j,'Расписание', next_day, mergeStatus, weekday_parse)
                    if type(schedule) == type(None):
                        print('Группа не найдена:', schedule)

                    else:
                        print('НАШЕЕЛ')
                        return (schedule)
                        break
                elif text == 'Замена' and text in j:
                    for i in self.file_name_list: 
                        if 'Расписание' in i:
                            print('\nОткрытие файла:', i)
                            schedule = read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False, mergeStatus, weekday_parse)
                            schedule_main = read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False, False, weekday_parse)
                            if type(schedule) == type(None):
                                print('Группа не найдена:', schedule)
                            else:
                                print(i)
                                if read_word.read_weekday(j) == read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False, mergeStatus, weekday_parse):
                                    return read_word.read_file(group, j, mergeStatus)
                                    break
        elif mergeStatus == True:
            Mschedule = ''
            Msubstitutions = ''
            Mtime = ''
            for n in range(0, 2):
                print('\n\n\n',n,'\n\n\n')
                Mtext = ''
                
                if n == 0: Mtext = 'Расписание'
                elif n == 1: Mtext = 'Замена'
                
                for j in self.file_name_list:
                    print("*********\n" + j)

                for j in self.file_name_list:
                    print('Отлажен')
                    if Mtext == 'Расписание' and Mtext in j:
                        print('[Merge True]Открытие файла:', j)
                        schedule = read_excel.main_open(group, j,'Расписание', False, mergeStatus, weekday_parse)
                        schedule_main = read_excel.main_open(group, j,'Узнать на какой день недели парсить замены', False, False, weekday_parse)
                        if type(schedule) == type(None):
                            print('Группа не найдена:', schedule)
                            
                        else:
                            Mschedule = schedule
                            print("Раписание найдено. Дальше парсим замены")
                            break
                    elif Mtext == 'Замена' and Mtext in j:
                        
                        for i in self.file_name_list: #ВТОРОЙ ЦИКЛ FIX
                            if 'Расписание' in i:
                                print('[Merge True]Открытие файла:', i)
                                
                                
                                schedule = read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False, False, weekday_parse)

                                print("[Merge find weekday] Парсим на ", schedule)
                                if type(schedule) == type(None):
                                    print('Группа не найдена:', schedule)
                                else:
                                    print(i)
                                    if read_word.read_weekday(j) == read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False, False, weekday_parse):
                                        otvet = read_word.read_file(group, j, mergeStatus)
                                        Msubstitutions = otvet[0]
                                        Mtime = otvet[1]
                                        break
                            

            if type(schedule_main) == type(None):
                schedule_main = read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False, False, False)
                print('День недели было пустое')
            else:
                print(schedule_main)
            return merge.merge(Mschedule, Msubstitutions, Mtime, schedule_main)



        if text == 'Расписание':
            return ('Агент не смог найти вашу группу в расписании. Обратитесь к моему начальству: vk.me/agent_nomer11')
        elif text == 'Замена':
            return ('Замен нет')
        else:
            return ('Произошло что-то невероятное! Скорее напишите нам: vk.me/agent_nomer11')
        """
        for item in schedule:
            for j in range(len(matrix)):
                matrix[j][0] = [item['title']]

            print()

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j], end = ' ')
            print()

        #for item in schedule:
        print('Найдено файлов на сайте:', len(schedule))
        """

    def parse(self, group, text, next_day, merge, weekday_parse):
        done_sc = []
        html = self.get_html(self.URL)
        if html.status_code == 200:
            #html = self.get_html(self.URL)
            
            with open('data.txt', encoding="utf-8") as json_file:
                data = json.load(json_file)
                for p in data:
                    done_sc.append({
                    'title': p['title'],
                    'link': p['link'],
                                })

            #print('LINK', [[d['link']] for d in done_sc])
            #print('ДАНОН:',done_sc)
            print('Контольная точка')
            with open('listfile.txt', 'r', encoding="utf-8") as filehandle:
                for line in filehandle:
                    # удалим заключительный символ перехода строки
                    currentPlace = line[:-1]
                    # добавим элемент в конец списка
                    self.file_name_list.append(currentPlace)
            return (self.file_search(group, done_sc, text, next_day, merge, weekday_parse))

        else:
            print('Error. Сайт не доступен')
            file_name_list = []
            for root, dirs, files in os.walk("."):  
                for filename in files:
                    filename = (((filename).replace('.xlsx', '')).replace('.docx', '')).replace('.xls', '')
                    file_name_list.append(filename)
                    #print(filename)

            with open('listfile.txt', 'w', encoding="utf-8") as filehandle:  
                    for listitem in file_name_list:
                        filehandle.write('%s\n' % listitem)

            with open('data.txt', encoding="utf-8") as json_file:
                data = json.load(json_file)
                for p in data:
                    done_sc.append({
                    'title': p['title'],
                    'link': p['link'],
                                })

            #print('LINK', [[d['link']] for d in done_sc])
            #print('ДАНОН:',done_sc)
            print('Контольная точка')
            with open('listfile.txt', 'r', encoding="utf-8") as filehandle:
                for line in filehandle:
                    # удалим заключительный символ перехода строки
                    currentPlace = line[:-1]
                    # добавим элемент в конец списка
                    self.file_name_list.append(currentPlace)
            
            return (self.file_search(group, done_sc, text, next_day, merge, weekday_parse) + ['\n\nСАЙТ НЕ ДОСТУПЕН. ЛОКАЛЬНОЕ РАСПИСАНИЕ'])
        return (self.text)


def test():
    file_name_list = []
    for root, dirs, files in os.walk("."):  
        for filename in files:
            (((filename).replace('.xlsx', '')).replace('.docx', '')).replace('.xls', '')
            file_name_list.append(filename)
            #print(filename)

    with open('listfile.txt', 'w', encoding="utf-8") as filehandle:  
            for listitem in file_name_list:
                filehandle.write('%s\n' % listitem)
#test()
#ps = parser('Расписание')
#print('\n\n\n**********\n\n\nРезультат который уйдет в вк:', ps.parse('3исп-9','Расписание', False, True))
#print('\n\n\n**********\n\n\nРезультат который уйдет в вк:', ps.parse('4исп-9', 'Расписание', False, True, 'нет'))