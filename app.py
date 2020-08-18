  
#Python libraries that we need to import for our bot
import random
from flask import Flask, request, Response
from pymessenger.bot import Bot
from wit import Wit
import requests
app = Flask(__name__)
# ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_TOKEN = 'EAAIbv66Rh8wBAB7Kuffsbq1AQCH63y4Tm1MyTFQE5ZB5394LII1kFPGxS0heZASXtkmWR56oJDtcT6pS5iheEf7ZAY5i2HwqWUQVdfe0HamWz0HILtlGFouSLWEixUlHfzJayG1tTj1Uk5dUgbnRQW10pkzxfuQroTmpn86Ut5A7i29Czva'
VERIFY_TOKEN = 'VERIFY_TOKEN'
WIT_TOKEN    = '6OGZVMSELXTJM5HVSWH2IRBRRMLNGKGK'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        """
        Handler for webhook (currently for postback and messages)
        """
        data = request.json
        if data['object'] == 'page':
            for entry in data['entry']:
                # get all the messages
                messages = entry['messaging']
                if messages[0]:
                    # Get the first message
                    message = messages[0]
                    # Yay! We got a new message!
                    # We retrieve the Facebook user ID of the sender
            
                    fb_id = message['sender']['id']
                    print('fb_id :', fb_id)
                    # We retrieve the message content
                    text = message['message']['text']
                    print('text:', text)
                    # Let's forward the message to Wit /message
                    # and customize our response to the message in handle_message
                    response = client.message(text)
                    # response ={'text': 'hello bot', 'intents': [{'id': '742387059668438', 'name': 'greating', 'confidence': 0.9787}], 'entities': {}, 'traits': {'wit$greetings': [{'id': '5900cc2d-41b7-45b2-b21f-b950d3ae3c5c', 'value': 'true', 'confidence': 0.9997}]}}
                    handle_message(response=response, fb_id=fb_id)
        else:

            return 'Received Different Event'
    return 'Message Processed!!!'


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + ACCESS_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content

def first_trait_value(traits, trait):
    """
    Returns first trait value
    """
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val


def handle_message(response, fb_id):
    """
    Customizes our response to the message and sends it
    """
    greetings = first_trait_value(response['traits'], 'wit$greetings')
    if greetings:
        text = "hello!"
    else:
        text = "We've received your message: " + response['text']
    # send message
    fb_message(fb_id, text)


@app.route("/", methods=['GET', 'POST'])
def show():
    return 'em đây là bot !!!!!!!'

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)
resp = client.message('hello bot!!! ')
print('Yay, got Wit.ai response: ' + str(resp))

if __name__ == "__main__":
    app.run(debug= True)