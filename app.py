'''
前端页面
'''
from flask import Flask, render_template, request
from output import answer
from classification import Question_classify
from AIML import Kernel

app = Flask(__name__)

qc = Question_classify()
bot = Kernel.Kernel()
bot.learn("cn-test.aiml")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(answer(userText, qc, bot))

if __name__ == "__main__":
    app.run()
