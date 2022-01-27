#-*- coding: UTF-8 -*-
'''
数据库调用模块
'''

import sqlite3
import time


#添加非AIML问答(专业知识)
def Insert_expert(dbname, question, answer, answer_type, predict_type):
    sql = "insert into log values(?, ?, ?, ?, ?, ?)"
    sql_id = "select max(logid) from log"
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute(sql_id)
    (id,) = cur.fetchone()
    if id is None:
        id = 1
    else:
        id = int(id)
        id = id + 1
    now = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cur.execute(sql, (id, question, answer, now, answer_type, predict_type))
    con.commit()
    con.close()


#添加AIML问答，即简单问候
def Insert_AIML(dbname, question, answer, answer_type):
    sql = "insert into log values(?, ?, ?, ?, ?, ?)"
    sql_id = "select max(logid) from log"
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute(sql_id)
    (id,) = cur.fetchone()
    if id is None:
        id = 1
    else:
        id = int(id)
        id = id + 1
    now = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cur.execute(sql, (id, question, answer, now, answer_type, None))
    con.commit()
    con.close()


#根据答案id获取答案和答案类型
def Query(dbname, id):
    sql = "select answer, feature from answer where aid = ?"
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute(sql, (id,))
    (answer,feature) = cur.fetchone()
    con.close()
    return answer, feature

if __name__ == '__main__':
    answer,feature = Query('qa.db', 1)
    print(answer)
    print(feature)
    Insert_AIML('qa.db', "你好", "再见", "AIML")
    Insert_expert('qa.db', "图书馆开放时间", answer,"业务问答", feature)