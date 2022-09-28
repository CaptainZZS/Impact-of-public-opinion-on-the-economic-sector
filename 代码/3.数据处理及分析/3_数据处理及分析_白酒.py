#成交额与成交量的关系为：成交数量（成交量）*成交价格=成交金额（成交额）
#通常人们说的大盘成交量指的是成交金额。成交额常常代表着市场的活跃度和资金规模。
import pandas as pd
import os
from matplotlib import pyplot as plt
import xlwt
# os.chdir(r'C:/Users/Captain/Desktop/舆论舆情对经济板块影响/数据/金融数据/白酒')
os.chdir(r'E:\Python编程\zzs_project\舆论舆情对经济板块影响\数据\金融数据\白酒')
#os.chdir(r'F:/Python编程/zzs_project/舆论舆情对经济板块影响/数据/金融数据/白酒')
dir = os.getcwd()
dirs = os.listdir(dir)

def operation1(filename):
    data = pd.DataFrame(pd.read_csv(filename))
    data_trade_date = list(data['trade_date'])
    data_close = list(data['close'])
    data_vol = list(data['vol'])
    return data_trade_date[::-1],data_close[::-1],data_vol[::-1]

def operation2(x,y1,y2):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体
    plt.rcParams['axes.unicode_minus'] = False  # 设置正负号
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('白酒')

    ax1.set_ylabel('总成交额')
    ax1.bar(range(len(x)),y2)

    ax2 = ax1.twinx()
    ax2.plot(range(len(x)), y1,color='r',linestyle='--')
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
    plt.savefig('E:/Python编程/zzs_project/舆论舆情对经济板块影响/数据/图/白酒/'+'白酒板块'+'.png')
    plt.show()

def main():
    data = pd.DataFrame(pd.read_csv(dirs[0]))
    length = len(list(data['trade_date']))
    listy1,listy2 = [0 for i in range(length)],[0 for i in range(length)]
    for i in range(len(dirs)):
        x,y1,y2 = operation1(dirs[i])
        for i in range(len(y1)):
            listy1[i] += float(y1[i])
            listy2[i] += float(y2[i])
    operation2(x,listy1,listy2)
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('sheet1')
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, '价格')
    sheet.write(0, 2, '成交额')

    for i in range(len(x)):
        sheet.write(i + 1, 0, x[i])
        sheet.write(i + 1, 1, listy1[i])
        sheet.write(i + 1, 2, listy2[i])

    workbook.save('E:/Python编程/zzs_project/舆论舆情对经济板块影响/数据/金融数据/白酒/白酒板块数据.xls')
    print('已将数据保存至excel！')


main()