# quantumtw
This project is developed by TENG-LIN YU. You can contact me by following methods:
- Mail: tlyu0419@gmail.com
- Facebook: https://www.facebook.com/tlyu0419

## requirements
- pip install requirements

## query_date
Unlike twstock packages, it requests the data by session.get() so that we don't need to sleep 5 seconds for each request.
Notice: You can't query data by the browser while running this function, or you will be banned by the website.

- query Highlights of Daily Trading
- query singal stock
- query Top 150 stocks 
- query specific stocks.

## trade_signals
- by Machine Learning model
  - timeseries
- by Domains

- Visualize Result


## News
- Yahoo market

## Notification
- Mail
  - If you only want to receive the result, you can send mail to me, and then I will send mail to you daily:)

## Announcement
It's just a toy project, the prediction of the stock price is based on historical data, but in fact, many circumstances could affect the stock price. 
2610 is a bad example; another is a good example
so the project only offers trade signals; you need to consider other information and then buy or sell your stock.

## Ref packages
- [Prophet](https://github.com/facebook/prophet)
- [FindMind](https://github.com/FinMind/FinMind)
- [FindLab](https://www.finlab.tw/)
  - [機器學習於量化交易的挑戰與解法 - 韓承佑 | MOPCON 2019](https://www.youtube.com/watch?v=27M-YV56xME)
   - How to label trade signals
   - variables