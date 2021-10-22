#-*- coding: UTF-8 -*-
'''
输出函数
'''
from db_fetch import Query, Insert_expert, Insert_AIML

def answer(question, qc, bot):
    if question == '':
        return '您的提问是空，你可以问点啥哦。'
    answer = bot.respond(question)
    answer_type = "AIML"
    if answer != '找不到答案':
        Insert_AIML('qa.db', question, answer, answer_type)
        return answer
    elif answer == '找不到答案':
        predict_id = qc.predict_NB(question)

        answer_type = "业务问答"
        answer,feature = Query('qa.db', int(predict_id))
        Insert_expert('qa.db', question, answer, answer_type, feature)
        return answer