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
        stock_data.to_csv('E:/Python编程/zzs_project/舆论舆情对经济板块影响/数据/金融数据/银行/'+stock_code+'.csv', header=True, index=False)

def main():
    stock_code_list = ['600036.SH', '601166.SH', '000001.SZ', '601398.SH', '002142.SZ', '601328.SH', '600000.SH',
                       '601288.SH', '600016.SH', '601229.SH']
    start_date = '20201207'
    end_date = '20211207'
    stock_data = obtain_stocks(start_date,end_date,stock_code_list)
    save_stock_data(stock_data)

main()