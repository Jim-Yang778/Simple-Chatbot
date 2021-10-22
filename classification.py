#-*- coding: UTF-8 -*-

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import jieba
#读取语料question.csv
def getfilelist(root_path):
    data = pd.read_csv(root_path, sep=',')
    id = []
    question = []
    for id_num in data['qid']:
        id.append(id_num)
    for question_content in data['content']:
        question.append(question_content)
    return id, question

#清除符号
def clean_content(content):
    clear_content = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", content)
    return clear_content

class Question_classify():
    def __init__(self):
        # 读取训练数据
        self.train_x,self.train_y=self.read_train_data()
        self.tv = TfidfVectorizer()
        self.model_NB = self.train_model_NB()

    # 获取训练数据
    def read_train_data(self):
        jieba.load_userdict("./data/userdict.txt")
        id, content = getfilelist('./data/question.csv')
        train_x = []
        train_y = id
        for question in content:
            question = clean_content(question)
            word_list = list(jieba.cut(str(question).strip()))
            # 将这一行加入结果集
            train_x.append(" ".join(word_list))
        return train_x, train_y

    # 训练模型
    def train_model_NB(self):
        X_train, y_train = self.train_x, self.train_y
        train_data = self.tv.fit_transform(X_train).toarray()
        clf = MultinomialNB(alpha=0.01)
        clf.fit(train_data, y_train)
        return clf

    # 预测
    def predict_NB(self,question):
        question = clean_content(question)
        question=[" ".join(list(jieba.cut(question)))]
        test_data=self.tv.transform(question).toarray()
        y_predict_NB = self.model_NB.predict(test_data)[0]
        return y_predict_NB


if __name__ == '__main__':
    #测试
    qc = Question_classify()
    print(qc.predict_NB("今天图书馆有什么活动"))
    print(qc.predict_NB("图书馆微信公众号是多少"))
    print(qc.predict_NB("图书借阅区在图书馆什么地方"))