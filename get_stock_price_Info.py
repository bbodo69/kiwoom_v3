import pandas as pd
import matplotlib.pyplot as plt
import requests
from matplotlib import dates as mdates
from bs4 import BeautifulSoup as bs
import os
import warnings
from datetime import datetime, date, timedelta
import exchange_calendars as ecals
from dateutil.relativedelta import relativedelta

######## FutureWarring 방지 ########
warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWarning 제거

######## 변수 ########
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
folder_path = "output/" + datetime.now().strftime('%Y-%m-%d')
code_filePath = "input/상장법인목록.xlsx"
code_sheetName = "상장법인목록"

######## 사전준비 ########
if not os.path.exists('output'):
    try:
        os.mkdir('output')
    except OSError as error:
        print(error)
if not os.path.exists(folder_path):
    try:
        os.mkdir(folder_path)
    except OSError as error:
        print(error)

######## 최근 1달 개장일 리스트 추출 ########
XKRX = ecals.get_calendar("XKRX")
df_date = pd.DataFrame(XKRX.schedule.loc[datetime.today()+ relativedelta(months=-1):datetime.today().strftime('%d.%m.%Y')])
date_list = []
for i in df_date['open']:
    date_list.append(i.strftime("%Y.%m.%d"))

######## 종목코드 불러오기 ########
df_codes = pd.read_excel(code_filePath, engine='openpyxl', sheet_name=code_sheetName, converters={'종목코드':str})

######## 종목별 가겨정보 가져오기 ########
for idx, row in df_codes.iterrows():
    df = pd.DataFrame()
    if '스팩' in str(row['회사명']):
        continue
    else:
        code = row['종목코드']

    for page in range(1, 3):
        page_url = 'https://finance.naver.com/item/sise_day.nhn?code={}&page={}'.format(code, page)
        response = requests.get(page_url, headers=headers)
        html = bs(response.text, 'html.parser')
        html_table = html.select("table")
        table = pd.read_html(str(html_table))
        df = df.append(table[0].dropna())
        if len(df) == 0:
            break
        df = df.dropna()
        df = df.sort_values(by='날짜')
        # 최근 30 일 데이터만 가져오기
        df[df['날짜'].isin(date_list)]
    print(5)
    filepath = os.path.join(folder_path, code+'.xlsx')
    print(6)
    if len(df) < 15:
        print(code)
    df.to_excel(filepath, index=False, sheet_name='sheet1')
    print(str(idx) + ' / ' + str(len(df_codes)) + ' 완료')
    
    
    
    

######## 이미지 저장 ########
# plt.figure(figsize=(15, 5))
# plt.title('stock price')
# plt.xticks(rotation=45)
# plt.plot(df['날짜'], df['종가'], 'co-')
# plt.grid(color='gray', linestyle='--')
# plt.show()