import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

url = 'https://ezone.iitp.kr/common/anno/list?cPage='

title_list =[]
url_list = []
type_list = []
start_list = []
end_list = []
deadline_list = []

def get_info(raw_row):
    type = raw_row.find_all('span')[0].text
    date = raw_row.find_all('div')[1].find_all('span')[2].find_all('strong')[0].find_all('span')[0].text[13:].replace("-","")
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')

    if type == '과제공고' : 
        int(date)
        if date > nowDate:
            deadline = int(date) - int(nowDate)
            
            title_list.append(raw_row.find_all('a')[0].text.replace("\t","").replace("\n","").replace("\r","").replace("\xa0",""))
            url_list.append('https://ezone.iitp.kr/' + raw_row.a['href'])
            type_list.append(raw_row.find_all('span')[0].text)
            start_list.append(raw_row.find_all('div')[1].find_all('span')[2].find_all('strong')[0].find_all('span')[0].text[:-13])
            end_list.append(raw_row.find_all('div')[1].find_all('span')[2].find_all('strong')[0].find_all('span')[0].text[13:])
            deadline_list.append(deadline)
        else :
            pass
    else :
        pass

for i in range(1, 21):
    url_temp = url+str(i)
    req = requests.get(url_temp)
    html = req.text
    status = req.status_code

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('ul.basic_bbs > li')

    print("-------------" + str(i) + "-------------")
    print("상태 : " + str(status))
    
    for i in range(1, len(title)) :
        year = title[i].find_all('div')[0].text.replace("\t","").replace("\n","").replace("\r","").replace("\xa0","")
        if year == '2020' :
            get_info(title[i])
        else :
            pass

df = pd.DataFrame(list(zip(title_list,url_list,type_list,start_list,end_list,deadline_list)), columns=['공고명','링크','공고유형','시작일','종료일','마감일'])
df.to_csv("iitp.csv",index=False,encoding='utf-8-sig')