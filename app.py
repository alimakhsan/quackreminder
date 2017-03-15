import os
import sys
import json
import string

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if 'show' in message_text.lower():
                        send_message(sender_id, "Here's your reminder")
                        three_generic(sender_id, "Meeting", "Tomorrow at 8 am", "mark as done", "reschedule", "delete")
                    elif 'main' in message_text.lower():
                        two_button(sender_id, "ayo gan!", "main sekarang", "main besok")
                    elif 'dota' in message_text.lower():
                        send_message(sender_id, "inget skripsi gan")
                    else:
                        send_message(sender_id, "sorry i didn't know")

                #if messaging_event.get("delivery"):  # delivery confirmation
                #    pass

                #if messaging_event.get("optin"):  # optin confirmation
                #    pass

                #if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                #    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text":message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def generic_no_button(recipient_id, message_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"template",
                "payload":{
                "template_type":"button",
                "text":message_text,
                "buttons":[
                    {
                        "type":"postback",
                        "title": button1,
                        "payload": None
                    }
                ]}
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def one_button(recipient_id, message_text, button1):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"template",
                "payload":{
                "template_type":"button",
                "text":message_text,
                "buttons":[
                    {
                        "type":"postback",
                        "title": button1,
                        "payload": None
                    }
                ]}
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def two_button(recipient_id, message_text, button1, button2):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"template",
                "payload":{
                "template_type":"button",
                "text":message_text,
                "buttons":[
                    {
                        "type":"postback",
                        "title": button1,
                        "payload": None
                    },
                    {
                        "type":"postback",
                        "title": button2,
                        "payload": None
                    }
                ]}
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def three_button(recipient_id, message_text, button1, button2, button3):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"template",
                "payload":{
                "template_type":"button",
                "text":message_text,
                "buttons":[
                    {
                        "type":"postback",
                        "title": button1,
                        "payload": None
                    },
                    {
                        "type":"postback",
                        "title": button2,
                        "payload": None
                    },
                    {
                        "type":"postback",
                        "title": button3,
                        "payload": None
                    }
                ]}
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        
def two_generic(recipient_id, title, subtitle, button1, button2):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"template",
                "payload":{
                "template_type":"generic",
                "elements":[
                    {
                    "title":title,
                    "subtitle": subtitle,
                    "buttons":[
                        {
                            "type":"postback",
                            "title": button1,
                            "payload": None
                        },{
                            "type":"postback",
                            "title": button2,
                            "payload": None
                        }              
                    ]}
                ]}
            }   
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def three_generic(recipient_id, title, subtitle, button1, button2, button3):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"template",
                "payload":{
                "template_type":"generic",
                "elements":[
                    {
                    "title":title,
                    "subtitle": subtitle,
                    "buttons":[
                        {
                            "type":"postback",
                            "title": button1,
                            "payload": None
                        },{
                            "type":"postback",
                            "title": button2,
                            "payload": None
                        },{
                            "type":"postback",
                            "title": button3,
                            "payload": None
                        }              
                    ]}
                ]}
            }   
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
