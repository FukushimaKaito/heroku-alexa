#!/usr/bin/env python
# coding: UTF-8

import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import urllib.request
import json
import dateutil.parser

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
    url = "http://ambidata.io/api/v2/channels/10905/data?readKey=7e7df40858ef249c&n=1"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    dtdata = dateutil.parser.parse(ambdata[0]['created'])
    msg = render_template('now', date=dtdata.strftime('%Y/%m/%d %H:%M:%S'),vib=ambdata[0]['d1'],light=ambdata[0]['d2'])
    return question(msg)
    
@ask.intent("AskLightIntent")
def vegilight(vegetable):
    if vagetable == "インゲン":
        return question("インゲン")
    else:
        return question("モヒカン")

if __name__ == '__main__':
    app.run(debug=True)
