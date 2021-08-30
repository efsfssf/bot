import requests, re
from bs4 import BeautifulSoup
import read_excel, read_word, merge

class parser:
    
    URL = 'https://web.archive.org/web/20210303082231/https://academicol.ru/students/schedule/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    HOST = 'https://academicol.ru/'
    
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
                    scLink = item.find('a', {'id': 'black'}).get('href')
                    scName = item.find('a', {'id': 'black'}).get_text()
                else:
                    continue
                
            else:
                continue
            schedule.append({
                'title': scName,
                'link': scLink,
            })
        print('ШЕНДУАШ:', schedule)
        return schedule
    
    def save_from_www(self, content, text):
        file_name_list = []
        for i in range(len(content)):
            #if text in content[i][0]:
            filename = content[i][0]
            file_name_list.append(filename)
            r = requests.get(content[i][1], allow_redirects=True)
            if r.status_code == 200:
                open(filename + '.' + content[i][1].split('.')[-1], 'wb').write(r.content)
            else:
                print('Error. Ссылка на скачивание не доступна')
            print()
        #print('Список файлов:', file_name_list)
        

    def file_search(self, group, schedule, text, mergeStatus):
        
        matrix = [[d['title'], d['link']] for d in schedule]
        #print(*map(' '.join, matrix), sep='\n')
        for i in range(len(matrix)):
            if text in matrix[i][0]:
                print(matrix[i][0])
            print()
        self.save_from_www(matrix, text)
        
        test_file_name_list = ['Замена_на_20_августа_2021_г..docx', 'Расписание_1_2_курсов_с_01_04_по_05_07_2021_1_поток', 'Расписание_1-4_курсов_с_01.04_по_05.07.2021_(2_поток)']

        if mergeStatus == False:
            print('Марг фолс')
            for j in test_file_name_list:
                if text == 'Расписание' and text in j:
                    print('Открытие файла:', j)
                    schedule = read_excel.main_open(group, j,'Расписание', mergeStatus)
                    if type(schedule) == type(None):
                        print('Группа не найдена:', schedule)
                        
                    else:
                        return schedule
                        break
                elif text == 'Замена' and text in j:
                    for i in test_file_name_list:
                        if 'Расписание' in i:
                            print('Открытие файла:', i)
                            schedule = read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', mergeStatus)
                            if type(schedule) == type(None):
                                print('Группа не найдена:', schedule)
                            else:
                                print(read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', mergeStatus))
                                if read_word.read_weekday(j) == read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', mergeStatus):
                                    print(type(read_word.read_file(group, j, mergeStatus)))
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
                for j in test_file_name_list:
                    print('Отлажен')
                    if Mtext == 'Расписание' and Mtext in j:
                        print('Открытие файла:', j)
                        schedule = read_excel.main_open(group, j,'Расписание', mergeStatus)
                        if type(schedule) == type(None):
                            print('Группа не найдена:', schedule)
                            
                        else:
                            Mschedule = schedule
                            break
                    elif Mtext == 'Замена' and Mtext in j:
                        for i in test_file_name_list:
                            if 'Расписание' in i:
                                print('Открытие файла:', i)
                                schedule = read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False)
                                if type(schedule) == type(None):
                                    print('Группа не найдена:', schedule)
                                else:
                                    print(i)
                                    if read_word.read_weekday(j) == read_excel.main_open(group, i,'Узнать на какой день недели парсить замены', False):
                                        otvet = read_word.read_file(group, j, mergeStatus)
                                        Msubstitutions = otvet[0]
                                        Mtime = otvet[1]
                                        break
            return merge.merge(Mschedule, Msubstitutions, Mtime)                            
                
            
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

    def parse(self, group, text, merge):

        html = self.get_html(self.URL)
        if html.status_code == 200:
            schedule = self.get_content(html.text)
            html = self.get_html(self.URL, params=None)
            done_sc = self.get_content(html.text)
            
            print('Группа в парсе:', group, 'Тип:', type(group))
            if not group:
                return 'Агент не знает какая у вас группа :(\nНапишите /start и укажите вашу группу'
            else:
                return (self.file_search(group, done_sc, text, merge))
                
        
        else:
            print('Error. Сайт не доступен')
            return 'Error. Сайт не доступен'
        return (self.text)
    


#ps = parser('Расписание')
#ps.parse('Расписание')