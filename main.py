#!/usr/bin/env python

import logging
from random import shuffle
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from sympy import sieve

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def introduction():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("YesIntent")
def start():
    start_msg = render_template('start')
    return question(start_msg)


# @ask.intent("AnswerIntent", convert={'prime': int})
# def answer(prime):
#     if type(prime) != int:
#     return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)
