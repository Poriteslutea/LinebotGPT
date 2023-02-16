import requests
from bs4 import BeautifulSoup
from random import randint

from collections import defaultdict
import re



# 取得網頁
response = requests.get('https://www.tenlong.com.tw/products/9787111648178')
soup = BeautifulSoup(response.text, "html.parser")



# Python程序員面試筆試寶典 - 先擷取目錄內容
table_contents = soup.find_all("div", class_="item-desc")[2]

# chapter name list
chapter = ['Python基礎題','Python進階題', '資料結構與演算法','資料庫相關','爬蟲','數據分析','Pandas','機器學習']

# Create dict with chapter title as key name, sub title as value
q_dict = defaultdict(list)
for i in range(1,9):
    ch = table_contents.findAll('p')[i]
    ch_qlist = ch.getText().split('\r\n')
    q_dict[chapter[i-1]] = ch_qlist

# 正規表達式
# role = re.compile(r'\d.\d.\d ')

# 處理與選擇資料
for k,v in q_dict.items():
    new_ques = []
    for ques in v:
        # if role.match(ques):
        ques = ques.split(' ')[1]
        ques = re.sub(r'\d+', '', ques)
        new_ques.append(ques)
    q_dict[k] = new_ques

def get_question(catagory, q_dict=q_dict):
    q_list = q_dict[catagory]
    idx = randint(0,len(q_list)-1)
    return q_list[idx]



