import os
import pandas as pd
import csv
import warnings
import calendar

def Dictionaries_operation(x,y,z):
    Dictionaries1 = [line.strip() for line in open(x, 'r',encoding='utf-8').readlines()]
    Dictionaries2 = [line.strip() for line in open(y, 'r',encoding='utf-8').readlines()]
    Dictionaries3 = [line.strip() for line in open(z, 'r',encoding='utf-8').readlines()]
    return Dictionaries1,Dictionaries2,Dictionaries3

def read_newscontects(path,x,y,z):
    path_1 = os.getcwd()[:36]
    data = pd.DataFrame(pd.read_csv(path,encoding='gbk'))
    data = data.dropna()
    data_contects = list(data['内容'])
    data_date = list(data['日期'])
    data_time = list(data['时间'])
    list_test = []
    for i in range(len(data_contects)):
        for a in x:
            if a in data_contects[i]:
                list_test.append([data_date[i],data_time[i],data_contects[i],'白酒'])
                break
        for b in y:
            if b in data_contects[i]:
                list_test.append([data_date[i],data_time[i],data_contects[i],'房地产开发'])
                break
        for c in z:
            if c in data_contects[i]:
                list_test.append([data_date[i],data_time[i],data_contects[i],'银行'])
                break
    f = open(path_1+'数据/新闻/时间标签新闻.csv','w',encoding='gbk',newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(['date','time',"contents", "category"])
    for i in list_test:
        csv_writer.writerow(i)
    f.close()
    data = pd.DataFrame(pd.read_csv(path_1+'数据/新闻/时间标签新闻.csv',encoding='gbk'))
    return data

def Weight_calculation(data,x,y,z):
    list_date,list_category = list(data['date']),list(data['category'])
    x_date,x_price = list(x['日期']),list(x['价格'])
    y_date,y_price = list(y['日期']),list(y['价格'])
    z_date,z_price = list(z['日期']),list(z['价格'])
    list_emotion = [0 for i in range(len(list_date))]
    for i in range(len(list_date)):
        if list_category[i] == '白酒':
            try:
                x_index = x_date.index(int(date_weekday(list_date[i])))
                weight = calculation(x_index, x_price, x_date)
                if weight > 0:
                    list_emotion[i] = 1
                elif weight < 0:
                    list_emotion[i] = -1
            except:
                print(str(int(list_date[i])) + '这个日期找不到！')
                continue

        elif list_category[i] == '房地产开发':
            try:
                y_index = y_date.index(int(date_weekday(list_date[i])))
                weight = calculation(y_index, y_price, y_date)
                if weight > 0:
                    list_emotion[i] = 1
                elif weight < 0:
                    list_emotion[i] = -1
            except:
                print(str(int(list_date[i])) + '这个日期找不到！')
                continue

        elif list_category[i] == '银行':
            try:
                z_index = z_date.index(int(date_weekday(list_date[i])))
                weight = calculation(z_index, z_price, z_date)
                if weight > 0:
                    list_emotion[i] = 1
                elif weight < 0:
                    list_emotion[i] = -1
            except:
                print(str(int(list_date[i])) + '这个日期找不到！')
                continue
    return list_emotion

def calculation(index,list_price,list_date):
    if index <= len(list_date)-5:
        weight = 0.4*(float(list_price[index+1])-float(list_price[index]))+0.3*(float(list_price[index+2])-float(list_price[index]))+0.2*(float(list_price[index+3])-float(list_price[index]))+0.1*(float(list_price[index+4])-float(list_price[index]))
    elif index == len(list_date)-4:
        weight = 0.4 * (float(list_price[index + 1]) - float(list_price[index])) + 0.3 * (
                    float(list_price[index + 2]) - float(list_price[index])) + 0.2 * (float(list_price[index + 3])-float(list_price[index]))
    elif index == len(list_date)-3:
        weight = 0.4 * (float(list_price[index + 1]) - float(list_price[index])) + 0.3 * (
                    float(list_price[index + 2]) - float(list_price[index]))
    elif index == len(list_date)-2:
        weight = 0.4 * (float(list_price[index + 1]) - float(list_price[index]))
    else:
        weight = 0
    return weight

def date_weekday(date):
    date = str(int(date))
    y = date[:4]
    m = date[4:6]
    d = date[6:]
    x = calendar.weekday(int(y),int(m),int(d))
    if int(x) == 5:
       return str(int(date)-1)
    elif int(x) == 6:
        return str(int(date)-2)
    else:
        return date

def Digitization(path1,path2,path3,data):
    path_1 = os.getcwd()[:36]
    data1 = pd.DataFrame(pd.read_csv(path1, encoding='gbk'))
    data2 = pd.DataFrame(pd.read_csv(path2, encoding='gbk'))
    data3 = pd.DataFrame(pd.read_csv(path3, encoding='gbk'))
    list_emotion = Weight_calculation(data,data1,data2,data3)
    data_news = pd.read_csv(path_1 + '数据/新闻/时间标签新闻.csv', encoding='gbk')
    data_news['emotion'] = list_emotion
    data_news.to_csv(path_1 + '数据/新闻/时间标签新闻.csv', mode='w', index=False)

def main():
    warnings.filterwarnings("ignore")
    x = os.getcwd()[:36]
    Dictionaries_path1 = x+'白酒.txt'
    Dictionaries_path2 = x+'房地产开发.txt'
    Dictionaries_path3 = x+'银行.txt'
    Dictionaries1,Dictionaries2,Dictionaries3 = Dictionaries_operation(Dictionaries_path1,Dictionaries_path2,Dictionaries_path3)
    newscontectspath = x+'数据\新闻\新浪财经新闻爬取四合一.csv'
    data_1 = read_newscontects(newscontectspath,Dictionaries1,Dictionaries2,Dictionaries3)
    path1 = x+'数据/金融数据/白酒/白酒板块数据.csv'
    path2 = x+'数据/金融数据/房地产开发/房地产开发板块数据.csv'
    path3 = x+'数据/金融数据/银行/银行板块数据.csv'
    Digitization(path1,path2,path3,data_1)
main()