import os
import jieba
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import warnings
import joblib
path_1 = os.getcwd()[:36]

def separate_words(data):
    global path_1
    content = list(data['contents'])  # 将文本内容转换为list格式
    # 读入停用词表
    stopwords = pd.read_csv(path_1+'Chinese_Stop_Words.txt', index_col=False, sep="\t", quoting=3, names=['stopword'],encoding='GBK')  # list
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
    data = pd.DataFrame(pd.read_csv(path_1 + '/数据/新闻/时间标签新闻1.csv', encoding='gbk'))
    contents_clean,all_words = separate_words(data)
    df_train = pd.DataFrame({"contents_clean":contents_clean,"emotion":data["emotion"]})
    df_train = shuffle(df_train)
    best_score = 0
    i = 0.15
    while i <= 0.5:
        x_train, x_test, y_train, y_test = train_test_split(df_train["contents_clean"].values,
                                                            df_train["emotion"].values, test_size=i)
        words_train = format_transform(x_train)
        vectorizer = TfidfVectorizer(analyzer='word', max_features=4000, ngram_range=(1, 3), lowercase=False)
        vectorizer.fit(words_train)  # 转为向量格式
        classifier = MultinomialNB(alpha=0.01)
        classifier.fit(vectorizer.transform(words_train), y_train)
        words_test = format_transform(x_test)
        score = classifier.score(vectorizer.transform(words_test), y_test)
        if score >= best_score:
            best_score = score
            joblib.dump(classifier, path_1 + 'Positive_and_negative_correlation.m')
        print("----------------------------------分类结果报告-----------------------------------------")
        print("正反相关预测准确率:" + str(score))
        y_predict = classifier.predict(vectorizer.transform(words_test))
        print(classification_report(y_test, y_predict))
        i += 0.01
    print("正反相关预测准确率:" + str(best_score))
main()