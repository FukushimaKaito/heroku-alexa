#!/usr/bin/env python
# coding: UTF-8

from flask import Flask, jsonify, request
import csv
import os
import urllib.request
import json
import dateutil.parser
import yaml
from jinja2 import Template
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

with (BASE_DIR / "templates.yaml").open(encoding="utf-8") as template_file:
    messages = yaml.safe_load(template_file)


def render_message(name, **context):
    return Template(messages[name]).render(**context)


def alexa_response(message):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": message},
            "shouldEndSession": False,
        },
    }

def introduction():
    return render_message("welcome")

def help():
    return render_message("help")

def now():
    url = ambidata_url(1)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    dtdata = dateutil.parser.parse(ambdata[0]['created'])
    return render_message("now", date=dtdata.strftime('%Y/%m/%d %H:%M:%S'), vib=ambdata[0]['d1'], light=ambdata[0]['d2'])
    
def vegilight(vegetable):
    # 24H = 1440min
    url = ambidata_url(1440)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    high,mid,low=0,0,0
    for i in range(1440):
        if ambdata[i]['d1'] > 1000:
            high += 1
        elif ambdata[i]['d1'] < 300:
            low += 1
        else:
            mid += 1

    with (BASE_DIR / "lightVegiClass.csv").open() as csvfile:
        ldata = csv.reader(csvfile)
        vegclass = [row for row in ldata]

    # positive class
    if vegetable in vegclass[0]:
        if high > 360:
            return render_message("light-just")
        elif high + mid > 360:
            return render_message("light-higher")
        else:
            return render_message("light-lack")
    # negative class
    elif vegetable in vegclass[2]:
        if high > 30 or mid > 180:
            return render_message("light-highest")
        elif high + mid > 60:
            return render_message("light-just")
        else:
            return render_message("light-lack")
    # half class
    elif vegetable in vegclass[1]:
        if high > 120 or mid > 180:
            return render_message("light-highest")
        elif high + mid > 300:
            return render_message("light-just")
        else:
            return render_message("light-lack")
    else:
        return render_message("light-missing", veg=vegetable)

def countcheck():
    # 24H
    url = ambidata_url(1440)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        ambdata = json.loads(res.read().decode('utf8'))

    high,mid,low=0,0,0
    for i in range(1440):
        if ambdata[i]['d1'] > 1000:
            high += 1
        elif ambdata[i]['d1'] < 300:
            low += 1
        else:
            mid += 1

    return render_message("count", high=high, mid=mid, low=low)


def ambidata_url(sample_count):
    channel_id = os.environ.get("AMBIDATA_CHANNEL_ID", "10905")
    read_key = os.environ["AMBIDATA_READ_KEY"]
    return (
        f"https://ambidata.io/api/v2/channels/{channel_id}/data"
        f"?readKey={read_key}&n={sample_count}"
    )


def handle_alexa(payload):
    request_data = payload.get("request", {})
    request_type = request_data.get("type")

    if request_type == "LaunchRequest":
        return alexa_response(introduction())

    if request_type != "IntentRequest":
        return alexa_response(render_message("help"))

    intent = request_data.get("intent", {})
    intent_name = intent.get("name")
    if intent_name == "AMAZON.HelpIntent":
        message = help()
    elif intent_name == "AskNowdata":
        message = now()
    elif intent_name == "AskLightIntent":
        slots = intent.get("slots", {})
        vegetable = slots.get("vegetable", {}).get("value", "")
        message = vegilight(vegetable)
    elif intent_name == "CountCheckIntent":
        message = countcheck()
    else:
        message = render_message("help")

    return alexa_response(message)


@app.post("/")
def alexa():
    payload = request.get_json(silent=True) or {}
    return jsonify(handle_alexa(payload))


def lambda_handler(event, context):
    expected_skill_id = os.environ.get("ALEXA_SKILL_ID")
    actual_skill_id = (
        event.get("session", {})
        .get("application", {})
        .get("applicationId")
    )
    if expected_skill_id and actual_skill_id != expected_skill_id:
        raise PermissionError("request is not from the configured Alexa skill")

    return handle_alexa(event)

if __name__ == '__main__':
    app.run(debug=True)
