import tushare as ts


token = "6385a53ce90d6a4150b1195cdbea93010306ed3786425af6cdb59b60"
pro = ts.pro_api(token)

def obtain_stocks(start_date, end_date, stock_code_list=None):
    if stock_code_list is None:
        stock_code_list = pro.stock_basic(list_status='L').ts_code
    stock_data = {}
    for stock_code in stock_code_list:
        stock_data[stock_code] = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    return stock_data

def save_stock_data(all_stocks_data):
    for stock_code, stock_data in all_stocks_data.items():
        #stock_data.to_csv('E:/Python编程/zzs_project/舆论舆情对经济板块影响/数据/金融数据/房地产开发/'+stock_code+'.csv', header=True, index=False)
        stock_data.to_csv('F:/Python编程/zzs_project/舆论舆情对经济板块影响/数据/金融数据/房地产开发/'+stock_code+'.csv', header=True, index=False)

def main():
    stock_code_list = ['600048.SH', '600383.SH', '601155.SH', '600606.SH', '600641.SH', '600208.SH', '600773.SH',
                       '600848.SH', '600663.SH', '601668.SH']
    start_date = '20201207'
    end_date = '20211207'
    stock_data = obtain_stocks(start_date,end_date,stock_code_list)
    save_stock_data(stock_data)

main()