#-*- coding: UTF-8 -*-
'''
计算准确率
'''
import pandas as pd
import re
import jieba
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 获取问题文件，返回问题id列表和问题列表
def getfilelist(root_path):
    data = pd.read_csv(root_path, sep=',')
    id = []
    question = []
    for id_num in data['qid']:
        id.append(id_num)
    for question_content in data['content']:
        question.append(question_content)
    return id, question

def clean_content(content):
    clear_content = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", content)
    return clear_content

# 获取训练数据
def read_train_data(question_path):
    jieba.load_userdict("./data/userdict.txt")
    id, content=getfilelist(question_path)
    train_x = []
    train_y = id
    for question in content:
        question = clean_content(question)
        word_list = list(jieba.cut(str(question).strip()))
        # 将这一行加入结果集
        train_x.append(" ".join(word_list))
    return train_x, train_y

# 训练模型-NB
def train_model_NB(x_train, y_train):
    clf = MultinomialNB(alpha = 0.01)
    clf.fit(x_train, y_train)
    return clf

# 检测准确率-NB
def test_accuracy_nb(x, y):
    tv = TfidfVectorizer()
    x = tv.fit_transform(x).toarray()
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=16)
    clf = train_model_NB(xtrain, ytrain)
    ypred = clf.predict(xtest)
    accuracy = accuracy_score(ytest, ypred)
    accurate = str(accuracy * 100) + '%'
    print(accurate)

if __name__ == '__main__':
    path = './data/question.csv'
    x, y = read_train_data(path)
    test_accuracy_nb(x, y)
