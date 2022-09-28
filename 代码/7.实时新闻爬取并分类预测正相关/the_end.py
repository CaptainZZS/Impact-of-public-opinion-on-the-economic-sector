#encoding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import jieba,joblib,os,time,warnings
import pandas as pd

warnings.filterwarnings("ignore")
path_1 = os.getcwd()[:36]
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://finance.sina.com.cn/7x24/?tag=0"
driver.get(url)
time.sleep(5)
list_news = ['']

def News_real_time_crawling():
    global list_news
    driver.refresh()
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    message = soup.find(name='div', class_="bd_i_txt")
    list_news.insert(0,message.find('p',class_='bd_i_txt_c').string)
    return list_news

def format_transform(x): #x是数据集（训练集或者测试集）
    words =[]
    for line_index in range(len(x)):
        try:
            words.append(" ".join(x[line_index]))
        except:
            print("数据格式有问题")
    return words

def separate_words(data):
    # 读入停用词表
    x = os.getcwd()[:36]
    stopwords = pd.read_csv(x+'/Chinese_Stop_Words.txt', index_col=False, sep="\t", quoting=3, names=['stopword'],encoding='GBK')  # list
    stopwords = list(stopwords['stopword'])
    print("正在分词,请耐心等候......")
    contents_clean = []
    all_words = []
    for line in data:
        current_segment = jieba.lcut(line)  # jieba分词
        current_segment = [x.strip() for x in current_segment if x.strip() != '']  # 去掉分词后出现的大量空字符串
        if len(current_segment) > 1 and current_segment != "\r\n":
            line_clean = []
            for word in current_segment:
                if word in stopwords:
                    continue
                line_clean.append(word)
                all_words.append(str(word))
            contents_clean.append(line_clean)
    print('------------分词完成-----------')
    return contents_clean, all_words

while True:
    list_news = News_real_time_crawling()
    if list_news[0] == list_news[1]:
        print("没有最新的新闻！！！")
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print()
    else:
        print("有最新的新闻哦！！！")
        vectorizer = joblib.load(path_1 + "/最优模型/vectorizer.m")
        contents_clean, all_words = separate_words(list_news[:-1])
        mark1 = pd.DataFrame({"contents_clean": contents_clean})
        mark2 = mark1["contents_clean"].values
        words = format_transform(mark2)
        classification_model = joblib.load(path_1+"/最优模型/News_classifications.m")
        correlation_model = joblib.load(path_1+"/最优模型/Positive_and_negative_correlation.m")
        result1 = classification_model.predict(vectorizer.transform(words))
        if result1[0] == 1:
            print('这是白酒的新闻!')
            print(list_news[0])
            result2 = correlation_model.predict(vectorizer.transform(words))
            if result2[0] == 1:
                print("这是积极的新闻哦！！！")
            else:
                print("这是消极的新闻哦！！！")
        elif result1[0] == 2:
            print('这是房地产开发的新闻!')
            print(list_news[0])
            result2 = correlation_model.predict(vectorizer.transform(words))
            if result2[0] == 1:
                print("这是积极的新闻哦！！！")
            else:
                print("这是消极的新闻哦！！！")
        elif result1[0] == 3:
            print('这是银行的新闻!')
            print(list_news[0])
            result2 = correlation_model.predict(vectorizer.transform(words))
            if result2[0] == 1:
                print("这是积极的新闻哦！！！")
            else:
                print("这是消极的新闻哦！！！")
        else:
            print('这是其他板块的新闻!')
            print(list_news[0])
            print('我们不预测哦！')
        print()
    time.sleep(0.5)