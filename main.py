#!/usr/bin/env python

import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def introduction():
    msg = render_template('welcome')
    return question(msg)

@ask.intent("AMAZON.HelpIntent")
def help():
    msg = render_template('help')
    return question(msg)

@ask.intent("AskNowdata")
def now():
    data = createdata()
    msg = render_template('now', date=data[0]['created'],vib=data[0]['d1'],light=data[0]['d2'])
    return question(msg)
    
if __name__ == '__main__':
    app.run(debug=True)
