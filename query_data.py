import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import datetime

headers={'Referer': 'https://pchome.megatime.com.tw/'}

# 近期台股交易資訊
def get_stockinfo(stockid, start, end):
    '''
    stockid: input stock id
    start: Like '2021-01-01', default is L24M
    end: Like '2021-01-01', default is today
    '''
    yms =pd.date_range(start=start, end=end, freq='MS')
    df = [] 
    n = 0
    break_times = 0
    while n < len(yms):
        ym = yms[n]
        if n % 6 ==0:
            rs = requests.session()
            # Sleep 15 seconds, and then create a new session.
            time.sleep(15)
        try:
            url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={}&stockNo={}'.format(ym.strftime('%Y%m%d'), str(stockid))
            print(url)
            data = rs.get(url)
            ndf = pd.DataFrame(data=data.json()['data'], columns=data.json()['fields'])
            ndf['title'] = data.json()['title']
            df.append(ndf)
            n += 1
            break_times = 0
        except:
            break_times +=1
            if break_times >= 10:
                break
            print('ERROR and Retry:', stockid)
            
    df = pd.concat(df, ignore_index=True)
    
    df['STOCKID'] = df['title'].apply(lambda x: x.split(' ', -1)[1])
    df['STOCKNAME'] = df['title'].apply(lambda x: x.split(' ', -1)[2])
    df['日期'] = df['日期'].apply(lambda x: x.replace(x[:3], str(int(x[:3])+1911)))
    df['日期'] = df['日期'].apply(lambda x: re.sub(r'/', '-', x))
    df = df.loc[:,['STOCKID', 'STOCKNAME', '日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']]
    df = df.rename(columns={'日期': 'DATE',
                            '成交股數': 'TRADEVOLUME',
                            '成交金額': 'TRADEVALUE',
                            '開盤價':'OPENINGPRICE',
                            '最高價':'HIGHESTPRICE',
                            '最低價':'LOWESTPRICE',
                            '收盤價':'CLOSINGPRICE',
                            '漲跌價差':'CHANGE',
                            '成交筆數':'TRANSACTION'})
    df['TRADEVOLUME'] = df['TRADEVOLUME'].apply(lambda x: int(re.sub(',', '', x)))
    df['TRADEVALUE'] = df['TRADEVALUE'].apply(lambda x: int(re.sub(',', '', x)))
    df['OPENINGPRICE'] = df['OPENINGPRICE'].apply(lambda x: float(re.sub(',', '', x)))
    df['HIGHESTPRICE'] = df['HIGHESTPRICE'].apply(lambda x: float(re.sub(',', '', x)))
    df['LOWESTPRICE'] = df['LOWESTPRICE'].apply(lambda x: float(re.sub(',', '', x)))
    df['CLOSINGPRICE'] = df['CLOSINGPRICE'].apply(lambda x: float(re.sub(',', '', x)))
#     df['CHANGE'] = df['CHANGE'].apply(lambda x: float(re.sub(',', '', x)))
    df['TRANSACTION'] = df['TRANSACTION'].apply(lambda x: int(re.sub(',', '', x)))
    
    df['UPDATETIME'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return df

# top 150的台股
def top150_stocklist(stock_type = 'sotck', sort_by='volume'):
    '''
    stock_type: 'sotck' or 'OTC'(over-the-counter market). Default is 'stock'.
    sort_by: You can sort by 'volume'('成交量'),  'turnover'(成交金額), 'price'(成交價). Default is 'volume'.
    '''
    
    stock_type_no = 0 if stock_type == 'sotck' else 1
    sort_by_no = 0 if sort_by == 'volume' else 1

    df = []
    # 上市
    for page in list(range(1,6)):
        url = 'https://pchome.megatime.com.tw/rank/sto{}/ock0{}_{}.html'.format(stock_type_no, sort_by_no, page)
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text,features='lxml')
        soup = soup.find('div',{'id':'rank_table'}).findAll('tr',{'style':'background:white'})
        for data in soup:
            df.append([ele.text for ele in data.findAll('td',{'class':'ct'})])

    df = pd.DataFrame(df, columns = ['rank', 'stock', 'volume', 'price','change','change_rate','highest','lowest'])
    df['stock'] = df['stock'].apply(lambda x: re.sub('　| ', '', x))
    df['stock_name'] = df['stock'].apply(lambda x: x.split(r'(')[0])
    df['stock_id'] = df['stock'].apply(lambda x: re.findall('(\d+)', x)[0])
    df = df.loc[:,['rank', 'stock_id', 'stock_name', 'volume', 'price', 'change', 'change_rate', 'highest', 'lowest']]
    df
    return df

# Highlights of Daily Trading(大盤)
def get_dailytrading(start, end):
    '''
    start: Like '2021-01-01', default is L24M
    end: Like '2021-01-01', default is today
    '''
    yms =pd.date_range(start=start, end=end, freq='MS')
    df = [] 
    n = 0
    break_times = 0
    while n < len(yms):
        ym = yms[n]
        if n % 6 ==0:
            rs = requests.session()
            # Sleep 15 seconds, and then create a new session.
            time.sleep(15)
        try:
#             url = 'https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date={}'.format(ym.strftime('%Y%m%d'))
            url = 'https://www.twse.com.tw/en/exchangeReport/FMTQIK?response=json&date={}'.format(ym.strftime('%Y%m%d'))
            
            
            print(url)
            data = rs.get(url)
            ndf = pd.DataFrame(data=data.json()['data'], columns=data.json()['fields'])
            ndf['title'] = data.json()['title']
            df.append(ndf)
            n += 1
            break_times = 0
        except:
            break_times +=1
            if break_times >= 10:
                break
            print('ERROR and Retry:', stockid)
            
    df = pd.concat(df, ignore_index=True)
    
#     df['日期'] = df['日期'].apply(lambda x: x.replace(x[:3], str(int(x[:3])+1911)))
    df = df.rename(columns={'Date': 'DATE', # 日期
                            'title': 'TITLE',
                            'Trade Volume': 'TRADEVOLUME', # 成交股數
                            'Trade Value': 'TRADEVALUE', # 成交金額
                            'Transaction':'TRANSACTION', # 成交筆數
                            'TAIEX':'TAIEX', # 發行量加權股價指數
                            'Change':'CHANGE'} # 漲跌點數
                  )
    df = df.loc[:,['TITLE', 'DATE', 'TRADEVOLUME', 'TRADEVALUE', 'TRANSACTION', 'TAIEX', 'CHANGE']]
    df['TITLE'] = 'Highlights of Daily Trading'
    df['DATE'] = df['DATE'].apply(lambda x: re.sub(r'/', '-', x))
    df['TRADEVOLUME'] = df['TRADEVOLUME'].apply(lambda x: int(re.sub(',', '', x)))
    df['TRADEVALUE'] = df['TRADEVALUE'].apply(lambda x: int(re.sub(',', '', x)))
    df['TRANSACTION'] = df['TRANSACTION'].apply(lambda x: float(re.sub(',', '', x)))
    df['TAIEX'] = df['TAIEX'].apply(lambda x: float(re.sub(',', '', x)))
    df['UPDATETIME'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return df


# Working day