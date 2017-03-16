import os
import sys
import json
import string

import requests
from flask import Flask, request
from util import *
import traceback
import random
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

    data = request.get_json()

    #words
    greetings = ['hi', 'hei', 'hai', 'hello', 'hy', 'oi']

    try:

        get_message(data)

        payload = request.get_data()
        sender, message = messaging_events(payload)

        #greetings
        if any(greeting == message.lower() for greeting in greetings):
            send_text_message(sender, "Hi there!")

        #help
        elif 'help' in message.lower():
            send_replies(
                sender, 
                "What can I help you?",
                [
                    quick_reply(
                        "show me examples",
                        "show me examples"),
                    quick_reply(
                        "my reminders",
                        "my reminders")
                ])

        #handle task 1   
        #handle task 2
        elif 'meeting' in message.lower():
            send_button_template_message(
                sender,
                "Ok. I will remind you to" + message.lower(),
                [
                    generate_button(
                        "reschedule",
                        "reschedule"),
                    generate_button(
                        "show my reminders",
                        "show my reminders")
                ])

        #show examples
        #handle task 3
        elif 'show' in message.lower() and 'example' in message.lower():
            send_carousel_items(
                sender,
                [
                    generate_carousel_items(
                    "You can say",
                    "Buy eggs at 10 am"),
                    generate_carousel_items(
                    "You can say",
                    "Do exercise at 6.00"),
                    generate_carousel_items(
                    "You can say",
                    "Call mother in 10 minutes")
                ])

        elif 'show' in message.lower() or 'schedule' in message.lower() or 'my reminder' in message.lower():
        send_carousel_items(
            sender,
            [
                generate_carousel_items_buttons(
                "Meeting",
                "Tomorrow, 8:00AM",
                [
                    generate_button(
                        "reschedule",
                        "reschedule"
                        ),
                    generate_button(
                        "mark as done",
                        "mark as done"
                        ),
                    generate_button(
                        "delete",
                        "delete"
                        )
                ]),
                generate_carousel_items_buttons(
                "Call Andi",
                "Today, 5:05PM",
                [
                    generate_button(
                        "reschedule",
                        "reschedule"
                        ),
                    generate_button(
                        "mark as done",
                        "mark as done"
                        ),
                    generate_button(
                        "delete",
                        "delete"
                        )
                ]),
                generate_carousel_items_buttons(
                "Jogging with Budi",
                "Sun, Mar 26, 6:00AM",
                [
                    generate_button(
                        "reschedule",
                        "reschedule"
                        ),
                    generate_button(
                        "mark as done",
                        "mark as done"
                        ),
                    generate_button(
                        "delete",
                        "delete"
                        )
                ]),
                generate_carousel_items_buttons(
                "Meet my lecturer",
                "Tue, Apr 18, 10:00AM",
                [
                    generate_button(
                        "reschedule",
                        "reschedule"
                        ),
                    generate_button(
                        "mark as done",
                        "mark as done"
                        ),
                    generate_button(
                        "delete",
                        "delete"
                        )
                ]),
            ])


        #handle task 4
        #handle task 5
        #handle task 6
        #handle task 7
        #handle task 8
        #handle task 9
        #handle task 10

    except:
        pass

    else:
            send_text_message(sender, "Sorry I'm just a little ducky")

    return "ok"

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
