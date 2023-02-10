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
folder_path = "C:/Users/82107/Desktop/주식/" + datetime.now().strftime('%Y-%m-%d')
urls = ["https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page=",
        "https://finance.naver.com/sise/sise_index_day.naver?code=KOSDAQ&page="]

######## 종목별 가겨정보 가져오기 ########
for url in urls:
    df = pd.DataFrame()

    for page in range(1, 3):
        page_url = url+str(page)
        response = requests.get(page_url, headers=headers)
        html = bs(response.text, 'html.parser')
        html_table = html.select("table")
        table = pd.read_html(str(html_table))
        df = df.append(table[0].dropna())
        df = df.dropna()
        df = df.sort_values(by='날짜')
        # 최근 30 일 데이터만 가져오기
    print(df)


    # filepath = os.path.join(folder_path, code+'.xlsx')
    # if len(df) < 15:
    #     print(code)
    # df.to_excel(filepath, index=False, sheet_name='sheet1')
    # print(str(idx) + ' / ' + str(len(df_codes)) + ' 완료')

    ######## 이미지 저장 ########
    plt.figure(figsize=(15, 5))
    plt.title('stock price')
    plt.xticks(rotation=45)
    plt.plot(df['날짜'], df['체결가'])
    plt.grid(color='gray', linestyle='--')
    plt.show()