import requests
from bs4 import BeautifulSoup

# 取得網頁
response = requests.get('https://www.tenlong.com.tw/products/9787111648178')
soup = BeautifulSoup(response.text, "html.parser")



# Python程序員面試筆試寶典 - 先擷取第二章內容
table_contents = soup.find_all("div", class_="item-desc")[2]
ch2 = table_contents.findAll('p')[1]
ch2_qlist = ch2.getText().split('\r\n')

q_2_6 = []
q_2_7 = []
q_2_8 = []
q_2_9 = []
for q in ch2_qlist:
    if q.startswith('2.6.') and '？' in q:
        qq = ''.join(q.split('？')[:-1] + ['?'])
        qq = qq.split(' ')[1]
        q_2_6.append(qq)
    elif q.startswith('2.7.'):
        qq = ''.join([i for i in q if not i.isdigit()])
        qq = qq.split(' ')[1]
        q_2_7.append(qq)
    elif q.startswith('2.8.'):
        qq = ''.join([i for i in q if not i.isdigit()])
        qq = qq.split(' ')[1]
        q_2_8.append(qq)
    elif q.startswith('2.9.'):
        qq = ''.join([i for i in q if not i.isdigit()])
        qq = qq.split(' ')[1]
        q_2_9.append(qq)
    elif q.startswith('2.9.'):
        qq = ''.join([i for i in q if not i.isdigit()])
        qq = qq.split(' ')[1]
        q_2_9.append(qq)       


ch2_dict = {'資料類型':q_2_6, '日期與時間':q_2_7, '流程控制語句':q_2_8, 'collection模組':q_2_9}
