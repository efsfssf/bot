import requests, re
from bs4 import BeautifulSoup

class praser:
    
    URL = 'https://web.archive.org/web/20210303082231/https://academicol.ru/students/schedule/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    HOST = 'https://academicol.ru/'
    
    def __init__(self, text):
        self.text = text
        parse(text)
    
    def get_html(url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r
    
    def get_content(html):
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
    
    def file_search(schedule, text):
        print(schedule)
        

    def parse(text):
        html = get_html(URL)
        if html.status_code == 200:
            schedule = get_content(html.text)
            html = get_html(URL, params=None)
            done_sc = get_content(html.text)
            
            print(done_sc)
            
            file_search(done_sc, text)
        
        else:
            print('Error')
    
        
