import pandas as pd
import matplotlib.pyplot as plt
import requests
from matplotlib import dates as mdates
from bs4 import BeautifulSoup as bs
import os
import warnings
from datetime import datetime
import exchange_calendars as ecals
from setuptools._distutils.msvc9compiler import Reg

######## FutureWarring 방지 ########
warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWarning 제거

######## 변수 ########
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
folder_path = "C:/Users/82107/Desktop/주식/" + datetime.now().strftime('%Y-%m-%d')
url_korea = ["https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page=",
        "https://finance.naver.com/sise/sise_index_day.naver?code=KOSDAQ&page="]
url_world = [
        "https://finance.naver.com/world/sise.naver?symbol=DJI@DJI",
        "https://finance.naver.com/world/sise.naver?symbol=NAS@IXIC",
        "https://finance.naver.com/world/sise.naver?symbol=SPI@SPX"]

plt.figure(figsize=(15, 5))
plt.title("Compare Index")
plt.xticks(rotation=45)

######## 한국 지수별 가격정보 가져오기 ########
for url in url_korea:
    df = pd.DataFrame()
    title = url.split("=")[1].split("&")[0].split("@")[0]

    for page in range(1, 3):
        page_url = url + str(page)
        response = requests.get(page_url, headers=headers)
        html = bs(response.text, 'html.parser')
        html_table = html.select("table")
        table = pd.read_html(str(html_table))
        df = df.append(table[0].dropna(), ignore_index=True)
        df = df.dropna()
    # df = df.sort_values(by='날짜', ascending=False)
    df = df.sort_values(by='날짜')
    # df = df.reset_index()
    print(df)

    # 정규값 구해주기
    df['Regular'] = 1.000

    # 중위값
    Regular = (df['체결가'].max() + df['체결가'].min())/2

    # df['Regular'] 값 삽입
    for idx, row in df.iterrows():
        df.loc[idx, 'Regular'] = round(row['체결가'] / Regular, 3)
        # row['Regular'] = round(row['체결가'] / Regular, 3)

    ######## 이미지 저장 ########

    plt.plot(df['날짜'], df['Regular'], label = title)
    plt.grid(color='gray', linestyle='--')

######## 종목별 가겨정보 가져오기 ########
for url in url_world:
    df_world = pd.DataFrame()
    title = url.split("=")[1].split("&")[0].split("@")[0]

    page_url = url
    response = requests.get(page_url, headers=headers)
    html = bs(response.text, 'html.parser')
    html_table = html.select_one("#dayTable")
    table = pd.read_html(str(html_table))
    df_world = df_world.append(table[0].dropna(), ignore_index=True)
    df_world = df_world.dropna()
    # df_world = df_world.sort_values(by='일자', ascending=False)
    df_world = df_world.sort_values(by='일자')
    # df_world = df_world.reset_index()
    print(df_world)

    # 정규값 구해주기
    df_world['Regular'] = 1.000

    # 중위값
    Regular = (df_world['종가'].max() + df_world['종가'].min()) / 2

    # df['Regular'] 값 삽입
    for idx, row in df_world.iterrows():
        df_world.loc[idx, 'Regular'] = round(row['종가'] / Regular, 3)

        # '일자' + 1 = '날짜' -> plot 을 위한 날짜 통일
        df_world.loc[idx, '일자'] = df.loc[idx, '날짜']
        # row['Regular'] = round(row['체결가'] / Regular, 3)

    ######## 이미지 저장 ########
    # plt.figure(figsize=(15, 5))
    # plt.title(title)
    # plt.xticks(rotation=45)
    plt.plot(df_world['일자'], df_world['Regular'], label = title)
    plt.grid(color='gray', linestyle='--')

leg = plt.legend(loc='upper left')
plt.savefig('output/'+ str(df.loc[0, '날짜'])+'.png')