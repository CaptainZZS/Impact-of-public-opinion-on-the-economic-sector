#encoding:utf-8
#成交额与成交量的关系为：成交数量（成交量）*成交价格=成交金额（成交额）
#通常人们说的大盘成交量指的是成交金额。成交额常常代表着市场的活跃度和资金规模。
import pandas as pd
import os
from matplotlib import pyplot as plt
import xlwt
path_first = os.getcwd()[:36]


def Public_opinion_data(path):
    data = pd.DataFrame(pd.read_csv(path, encoding='utf-8'))
    list_date, list_category,list_emotion = list(data['date']), list(data['category']),list(data['emotion'])
    return list_date, list_category,list_emotion

def operation1(filename):
    data = pd.DataFrame(pd.read_csv(filename,encoding='gbk'))
    data_trade_date = list(data['日期'])
    data_close = list(data['价格'])
    data_vol = list(data['成交额'])
    return data_trade_date,data_close,data_vol

def operation2(x,y1,y2,path,n):
    global path_first
    list_date, list_category, list_emotion = Public_opinion_data(path)
    list_x_positive,list_y_positive = [],[]
    list_x_negative,list_y_negative = [],[]
    for i in range(len(list_date)):
        if list_category[i] == operation3(n):
            try:
                x_index = x.index(int(list_date[i]))
                if list_emotion[i] == 1:
                    list_x_positive.append(x_index)
                    list_y_positive.append(y1[x_index])
                    print(y1[x_index])
                elif list_emotion[i] == -1:
                    list_x_negative.append(x_index)
                    list_y_negative.append(y1[x_index])
            except:
                print(str(int(list_date[i])) + '这个日期找不到！')
                continue
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体
    plt.rcParams['axes.unicode_minus'] = False  # 设置正负号
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title(operation3(n))
    ax1.set_ylabel('总成交额')
    ax1.bar(range(len(x)), y2)
    ax2 = ax1.twinx()
    ax2.plot(range(len(x)), y1, color='r', linestyle='--')
    ax2.scatter(list_x_positive, list_y_positive, color='r')
    ax2.scatter(list_x_negative, list_y_negative, color='g')
    ax2.set_xlabel('交易日期')
    ax2.set_ylabel('交易收盘价格')
    x_ticks_label = [x[i] for i in range(0, len(x), 10)]
    ax2.set_xticks(range(0, len(x), 10))
    ax2.set_xticklabels(x_ticks_label)

    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    maxsize = 10
    m = 0.2
    N = len(x)
    s = maxsize / plt.gcf().dpi * N + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]

    plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    plt.savefig(path_first + '/数据/图/舆论对板块影响可视图/'+operation3(n)+'板块' + '.png')
    plt.show()

def operation3(x):
    if x == 0:
        return '白酒'
    elif x== 1:
        return '房地产开发'
    else:
        return '银行'

def main():
    list_path = [path_first+'/数据/金融数据/白酒/白酒板块数据.csv',path_first+'/数据/金融数据/房地产开发/房地产开发板块数据.csv',path_first+'/数据/金融数据/银行/银行板块数据.csv']
    path = path_first+'/数据/新闻/时间标签新闻.csv'
    for i in range(len(list_path)):
        x,y1,y2 = operation1(list_path[i])
        operation2(x,y1,y2,path,i)
main()