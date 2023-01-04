import os
import sys
from flask import Flask, request
from pymessenger import Bot
import requests

from assets import button_template_assets
from template import elements


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAJCagzDzgkBALHRu7mTT9QSDZAE1Qrkfo7pSkbai7rx7BgfIjyAZAA7Xe1ZBCVZARH9YfhPidyf99D07HNuFNez0xCSOxL4Xl3e9sxRDZCFoGaCuKwnRXPANApI3fjl17TLAJiotyP4rIYt4bN1VTTs2rWY7OEAoN0mqDZAA8u4YAqCzGgrWn"
API = "https://graph.facebook.com/v13.0/me/messages?access_token="+PAGE_ACCESS_TOKEN

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "bosa":
            return 'Verification token mismatch', 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                if messaging_event.get('postback'):
                    if 'title' in messaging_event['postback']:
                        messaging_postback = messaging_event['postback']['title']
                        if messaging_postback == "Get Started":
                            request_body = {
                                "recipient": {
                                    "id": sender_id
                                },
                                "message": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                            "template_type": "button",
                                            "text": "What do you want to do next?",
                                            "buttons": [
                                                {
                                                    "type": "web_url",
                                                    "url": "https://www.messenger.com",
                                                    "title": "Visit Messenger"
                                                },
                                                {
                                                    "type": "web_url",
                                                    "url": "https://www.youtube.com",
                                                    "title": "Visit Youtube"
                                                },
                                            ]
                                        }
                                    }
                                }
                            }
                            response = requests.post(
                                API, json=request_body).json()
                            return response

                        elif messaging_postback == "Bosa":
                            request_body = {
                                "recipient": {"id": sender_id},
                                "message": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                            "template_type": "generic",
                                            "text": "Dummy",
                                            "elements": [
                                                {
                                                    "buttons": [
                                                        {
                                                            "type": "postback",
                                                            "title": "Get Started",
                                                            "payload": "DEVELOPER_DEFINED_PAYLOAD",
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                elif messaging_event.get('message'):
                    if "text" in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                        if messaging_text == "start":

                            request_body = {
                                "recipient": {
                                    "id": sender_id
                                },
                                "message": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                            "template_type": "button",
                                            "text": button_template_assets['button_text'],
                                            "buttons": [
                                                {
                                                    "type": "postback",
                                                    "title": button_template_assets['button_message'],
                                                    "payload":"USER_DEFINED_PAYLOAD"
                                                },
                                            ]
                                        }
                                    }
                                }
                            }
                            bot.send_text_message(sender_id, "Hello")
                            bot.send_generic_message(
                                sender_id, elements)
                            response = requests.post(
                                API, json=request_body).json()
                            return response

                        else:
                            response = "Please type 'start' to proceed."
                            bot.send_text_message(sender_id, response)

    return 'ok', 200


if __name__ == '__main__':
    app.run(debug=True, port=80)
