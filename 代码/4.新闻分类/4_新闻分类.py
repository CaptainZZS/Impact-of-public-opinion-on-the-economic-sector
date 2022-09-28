import os
import jieba
import pandas as pd
import csv
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.metrics import classification_report
import warnings
import joblib

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
    list_test = []
    for i in range(len(data_contects)):
        mark1 = 1
        for a in x:
            if a in data_contects[i]:
                list_test.append([data_contects[i],'白酒'])
                mark1 = 0
                break
        for b in y:
            if b in data_contects[i]:
                list_test.append([data_contects[i],'房地产开发'])
                mark1 = 0
                break
        for c in z:
            if c in data_contects[i]:
                list_test.append([data_contects[i],'银行'])
                mark1 = 0
                break
        if mark1:
            list_test.append([data_contects[i],'其他'])

    f = open(path_1+'数据/新闻/标签新闻2.csv','w',encoding='utf-8',newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(["contents", "category"])
    for i in list_test:
        csv_writer.writerow(i)
    f.close()
    data = pd.DataFrame(pd.read_csv(path_1+'数据/新闻/标签新闻2.csv',encoding='utf-8'))
    return data

def separate_words(data):
    content = list(data['contents'])  # 将文本内容转换为list格式
    # 读入停用词表
    x = os.getcwd()[:36]
    stopwords = pd.read_csv(x+'Chinese_Stop_Words.txt', index_col=False, sep="\t", quoting=3, names=['stopword'],encoding='GBK')  # list
    stopwords = list(stopwords['stopword'])
    print("正在分词,请耐心等候......")
    contents_clean = []
    all_words = []

    for line in content:
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

def format_transform(x): #x是数据集（训练集或者测试集）
    words =[]
    for line_index in range(len(x)):
        try:
            words.append(" ".join(x[line_index]))
        except:
            print("数据格式有问题")
    return words


def main():
    warnings.filterwarnings("ignore")
    x = os.getcwd()[:36]
    Dictionaries_path1 = x+'白酒.txt'
    Dictionaries_path2 = x+'房地产开发.txt'
    Dictionaries_path3 = x+'银行.txt'
    Dictionaries1,Dictionaries2,Dictionaries3 = Dictionaries_operation(Dictionaries_path1,Dictionaries_path2,Dictionaries_path3)
    newscontectspath = x+'数据\新闻\新浪财经新闻爬取四合一.csv'
    data_1 = read_newscontects(newscontectspath,Dictionaries1,Dictionaries2,Dictionaries3)
    contents_clean,all_words = separate_words(data_1)
    df_train = pd.DataFrame({"contents_clean":contents_clean,"label":data_1["category"]})
    label_mappping = {'白酒': 1, '房地产开发': 2, '银行': 3,'其他':4}
    df_train["label"] = df_train["label"].map(label_mappping)
    df_train = shuffle(df_train)
    best_score = 0
    i = 0.15
    while i <= 0.5:
        x_train, x_test, y_train, y_test = train_test_split(df_train["contents_clean"].values, df_train["label"].values,
                                                           test_size=i)
        words_train = format_transform(x_train)
        vectorizer = TfidfVectorizer(analyzer='word', max_features=4000, ngram_range=(1, 3), lowercase=False)
        vectorizer.fit(words_train)# 转为向量格式
        joblib.dump(vectorizer, x + 'vectorizer.m')
        classifier = MultinomialNB(alpha=0.01)
        classifier.fit(vectorizer.transform(words_train), y_train)
        words_test = format_transform(x_test)
        score = classifier.score(vectorizer.transform(words_test), y_test)
        if score >= best_score:
            best_score = score
            joblib.dump(classifier, x + 'News_classification.m')
        print("----------------------------------分类结果报告-----------------------------------------")
        print("分类准确率:" + str(score))
        y_predict = classifier.predict(vectorizer.transform(words_test))

        print(classification_report(y_test, y_predict))
        i += 0.01
    print(y_predict)
    print("分类准确率:" + str(best_score))
main()
