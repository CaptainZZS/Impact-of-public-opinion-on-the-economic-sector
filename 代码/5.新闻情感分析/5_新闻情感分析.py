import pandas as pd
import os
import csv
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
import jieba
from jieba import analyse

x = os.getcwd()[:36]
data = pd.read_csv(x+'数据/新闻/标签新闻.csv',encoding='utf-8')
data1 = data[['contents']]
data1.head(10)

data1['emotion'] = data1['contents'].apply(lambda x:SnowNLP(x).sentiments)

path_first = os.getcwd()[:36]
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
bins = np.arange(0,1.1,0.1)
plt.hist(data1['emotion'],bins,color='#4F94CD',alpha=0.9)
plt.xlim(0,1)
plt.xlabel('情感分')
plt.ylabel('数量')
plt.title('情感分直方图')
plt.savefig(path_first + '/数据/图/情感分析/情感分直方图板块' + '.png')
plt.show()

text = ''
for s in data['contents']:
    text += s

key_words = jieba.analyse.extract_tags(sentence=text, topK=10, withWeight=True, allowPOS=())
data2=data1[data1['emotion']<0.5]
text2 = ''
for s in data2['contents']:
    text2 += s
key_words = jieba.analyse.extract_tags(sentence=text2, topK=10, withWeight=True, allowPOS=())
pos = 0
neg = 0
for i in data1['emotion']:
    if i >= 0.5:
        pos += 1
    else:
        neg += 1
print('积极，消极数目分别为：',pos,neg)


plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

pie_labels='postive','negative'
plt.pie([pos,neg],labels=pie_labels,autopct='%1.1f%%',shadow=True)
plt.savefig(path_first + '/数据/图/情感分析/积极消极饼状图' + '.png')
plt.show()


data["emotion"] = data1['emotion']
for i in range(data.shape[0]):
    if data.loc[i,'emotion'] >= 0.5:
        data.loc[i, "emotion"] = 1
    else:
        data.loc[i, "emotion"] = 0

data.to_csv(x+'数据/新闻/标签新闻.csv',mode = 'w',index =False)

