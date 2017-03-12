import os
import sys
import json

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

                    send_message(sender_id, "got it, thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    try:
        payload = request.get_data()
        sender, message = messaging_events(payload)
        if message == "help":
            send_text_message(sender , "You can choose topic you would like to learn and practice from the menu on left. For more information you can drop us a message and we will reply back to you shortly. ")
        if message == "topics_to_learn":
            send_replies(
                sender, 
                "Select the topic you want to learn? 1.) Rational Numbers <br/> 2.) Linear Equation in One variable /n 3.) Understanding Quadrilaterals",
                [
                    quick_reply(
                        "1",
                        "rat"),
                    quick_reply(
                        "2",
                        "LINEAR"),
                    quick_reply(
                        "3",
                        "QUAD"),
                    quick_reply(
                        "4",
                        "BT"),
                    quick_reply(
                        "5",
                        "ON"),
                    quick_reply(
                        "6",
                        "LINEAR"),
                    quick_reply(
                        "7",
                        "QUAD"),
                    quick_reply(
                        "8",
                        "BT"),
                    quick_reply(
                        "more",
                        "BT")])

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
