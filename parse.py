import requests, re
from bs4 import BeautifulSoup

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
        
        return schedule
    
    def file_search(self, schedule, text):
        matrix =  ([['title'], ['link']])
        
        for item in schedule:
            for j in range(len(matrix)):
                matrix[j][0] = [item['title']]
                
            print()
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j], end = ' ')

        #for item in schedule:
        print('Найдено файлов на сайте:', len(schedule))
        

    def parse(self, text):
        
        html = self.get_html(self.URL)
        if html.status_code == 200:
            schedule = self.get_content(html.text)
            html = self.get_html(self.URL, params=None)
            done_sc = self.get_content(html.text)
            
            self.file_search(done_sc, text)
        
        else:
            print('Error')
        return (self.text)
    


ps = parser('Расписание')
ps.parse('Расписание')