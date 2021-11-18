# coding=utf-8
import requests, re, os, json
from bs4 import BeautifulSoup

class cronTask:

    URL = 'http://academicol.ru/students/schedule/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    HOST = 'http://academicol.ru/'
    html = None
    done_sc = None
    

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
    
    def save_file(self, filenameAndExpansion, r):
        print('Скачивание',filenameAndExpansion)
        open(filenameAndExpansion, 'wb').write(r.content)

    def find_error_link(self, content):
        for i in range(len(content)):
            #if text in content[i][0]:
            filename = content[i][0]
            self.file_name_list.append(filename)
            r = requests.get(content[i][1], allow_redirects=True)
            if r.status_code != 200:
                #если в ссылка ведет не на сайт колледжа
                content[i][1] = content[i][1].replace('http://academicol.ru/https://docs.google.com/viewer?url=','')
                
                    
            print()
    
    file_name_list = []
    def save_from_www(self, content):
        #ищем ошибки в ссылках
        self.find_error_link(content)

        print('Контент:', content)
        
        self.file_name_list.clear()
        for i in range(len(content)):
            #if text in content[i][0]:
            filename = content[i][0]
            print("ИМЯ:" + filename)
            
            self.file_name_list.append(filename)
            print('Список файлов1:', self.file_name_list)
            r = requests.get(content[i][1], allow_redirects=True)
            if r.status_code == 200:
                filenameAndExpansion = filename + '.' + content[i][1].split('.')[-1]

                files = os.listdir(os.getcwd())
                #print('Файлы', files)
                if not filenameAndExpansion in files:
                    self.save_file(filenameAndExpansion, r)
                else:
                    print(f'Файл {filenameAndExpansion} уже скачан')
                    
            else:
                print(f'Error. Ссылка на скачивание {content[i][1]} не доступна')
                #если в ссылка ведет не на сайт колледжа
                zamena = content[i][1].replace('http://academicol.ru/https://docs.google.com/viewer?url=','')
                print('После замены', zamena)
                r = requests.get(zamena, allow_redirects=True)
                filenameAndExpansion
                if r.status_code == 200:
                    print('Статус 200', 'Первый параметр', filenameAndExpansion, 'Второй параметр', r)
                    self.save_file(filenameAndExpansion, r)
                else:
                    print('Статус ошибки')
                    print(f'Error. Ссылка на скачивание {zamena} не доступна, даже после ВТОРОЙ попытки')
                    
            print()
        print('Список файлов:', self.file_name_list)
        with open('listfile.txt', 'w', encoding="utf-8") as filehandle:  
            for listitem in self.file_name_list:
                if not 'Расписание экзаменов' in listitem:
                    filehandle.write('%s\n' % listitem)



    def file_search(self,schedule):
        #print('Контент:', schedule)
        matrix = [[d['title'], d['link']] for d in schedule]
        #print(*map(' '.join, matrix), sep='\n')
        for i in range(len(matrix)):
            if 'Замена' in matrix[i][0] or 'Расписание' in matrix[i][0]:
                print(matrix[i][0])
            print()
        self.save_from_www(matrix)

    def start_cron(self):
        self.html = self.get_html(self.URL)
        if self.html.status_code == 200:
            self.done_sc = self.get_content(self.html.text)
            print('LINK', [[d['link']] for d in self.done_sc])
            
            path = r"D:\\бейкап\\Desktop\\bot0.9NEW\\data.txt"
            assert os.path.isfile(path)
            jstr = json.dumps(self.done_sc, indent=4, ensure_ascii=False)
            with open(path, 'w', encoding="utf-8") as outfile:
                json.dump(self.done_sc, outfile, ensure_ascii=False, indent=4)
            
            self.file_search(self.done_sc)
            print(jstr)
        else:
            print('Error. Сайт не доступен')

cr = cronTask('text')
cr.start_cron()