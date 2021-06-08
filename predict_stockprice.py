from prophet import Prophet
import datetime
import pandas as pd

# predict stickprice
def predict_stockprice(data, date_col, target_col, periods=100, future_data=None):
    '''
    data: Your current data to training model
    date_col: Date column name
    target_col: Target Variable columns name.
    periods: How many days you want to predict. Default is 100 Days.
    future_data: Future data you used for test the model accuracy.
    '''
    
    ndata = data.loc[:,[date_col, target_col]].rename(columns={date_col:'ds',
                                                               target_col:'y'})
    m = Prophet(yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True)
    m.fit(ndata)

    
    # Predict next 90D
    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)
    
    fig1 = m.plot(forecast)
    fig2 = m.plot_components(forecast)
    forecast['DATE'] = forecast['ds'].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'))
    
    # if exist
    if 'future_data' in locals():
        data['TYPE'] = 'CURRENT_DATA'
        future_data['TYPE'] = 'FUTURE_DATA'
        ndata = pd.concat([data, future_data], ignore_index=True)
        ndata = pd.merge(left=ndata, right=forecast, how = 'left', on='DATE')
        ndata['DATE'] = ndata['DATE'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
        print('Return A')
        return ndata
    else:
        print('Return B')
        return forecast
    
# Visualize prediction result
# import pandas as pd
# import seaborn as sns
# from sklearn.metrics  import r2_score
# from sklearn.metrics  import mean_absolute_error

# # Training data
# train_r2 = r2_score(y_true = result.loc[result['TYPE']=='CURRENT_DATA']['CLOSINGPRICE'],
#                     y_pred = result.loc[result['TYPE']=='CURRENT_DATA']['yhat'])
# train_mae = mean_absolute_error(y_true = result.loc[result['TYPE']=='CURRENT_DATA']['CLOSINGPRICE'],
#                                 y_pred = result.loc[result['TYPE']=='CURRENT_DATA']['yhat'])

# # Testing
# test_r2 = r2_score(y_true = result.loc[result['TYPE']=='FUTURE_DATA']['CLOSINGPRICE'],
#                    y_pred = result.loc[result['TYPE']=='FUTURE_DATA']['yhat'])

# test_mae = mean_absolute_error(y_true = result.loc[result['TYPE']=='FUTURE_DATA']['CLOSINGPRICE'],
#                                y_pred = result.loc[result['TYPE']=='FUTURE_DATA']['yhat'])

# print('R-Square on training data:', train_r2)
# print('MAE on training data:', train_mae)
# print('R-Square on test data:', test_r2)
# print('MAE on test data:', test_mae)

# dt = result.loc[:,['STOCKID', 'STOCKNAME', 'DATE', 'CLOSINGPRICE', 'yhat']]
# dt = pd.melt(dt, id_vars=['STOCKID', 'STOCKNAME', 'DATE'],var_name='TYPE', value_name='VALUE')
# sns.set(font_scale=1.5, style='whitegrid', rc={'figure.figsize':(20,6)})
# ax = sns.lineplot(x='DATE', y='VALUE', data=dt, hue='TYPE')
# ax = sns.scatterplot(x='DATE', y='CLOSINGPRICE', data=result, hue='TYPE')
# ax.fill_between(x='DATE', y1 = 'yhat_lower', y2='yhat_upper', data=result, alpha=0.2); 