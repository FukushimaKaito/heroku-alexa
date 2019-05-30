#!/usr/bin/env python
# coding: UTF-8

import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import csv
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
    # least
    url = "http://ambidata.io/api/v2/channels/10905/data?readKey=7e7df40858ef249c&n=1"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    dtdata = dateutil.parser.parse(ambdata[0]['created'])
    msg = render_template('now', date=dtdata.strftime('%Y/%m/%d %H:%M:%S'),vib=ambdata[0]['d1'],light=ambdata[0]['d2'])
    return question(msg)
    
@ask.intent("AskLightIntent")
def vegilight(vegetable):
    # 24H = 1440min
    url = "http://ambidata.io/api/v2/channels/10905/data?readKey=7e7df40858ef249c&n=1440"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    high,mid,low=0,0,0
    for i in range(1440):
        if ambdata[i]['d2'] > 1000:
            high += 1
        elif ambdata[i]['d2'] < 300:
            low += 1
        else:
            mid += 1

    with open("https://raw.githubusercontent.com/FukushimaKaito/heroku-alexa-py/master/lightVegiClass.csv") as csvfile:
        ldata = csv.reader(csvfile)
    vegclass = [row for row in ldata]

    # positive class
    if vegetable in vagclass[0]:
        if high > 360:
            msg = render_template('light-just')
            return question(msg)
        elif high + mid > 360:
            msg = render_template('light-higher')
            return question(msg)
        else:
            msg = render_template('light-lack')
            return question(msg)
    # negative class
    elif vegetable == vagclass[2]:
        if high > 30 or mid > 180:
            msg = render_template('light-highest')
            return question(msg)
        elif high + mid > 60:
            msg = render_template('light-just')
            return question(msg)
        else:
            msg = render_template('light-lack')
            return question(msg)
    # half class
    elif vegetable == vagclass[1]:
        if high > 120 or mid > 180:
            msg = render_template('light-highest')
            return question(msg)
        elif high + mid > 300:
            msg = render_template('light-just')
            return question(msg)
        else:
            msg = render_template('light-lack')
            return question(msg)
    else:
        msg = render_template('light-missing')
        return question(msg)

@ask.intent("CountCheckIntent")
def countcheck():
    # 24H
    url = "http://ambidata.io/api/v2/channels/10905/data?readKey=7e7df40858ef249c&n=1440"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    high,mid,low=0,0,0
    for i in range(1440):
        if ambdata[i]['d2'] > 1000:
            high += 1
        elif ambdata[i]['d2'] < 300:
            low += 1
        else:
            mid += 1

    msg = render_template('count',high=high,mid=mid,low=low)
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
