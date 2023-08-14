import os
import re
from token_file import Slack_Bot_Token
from token_file import Socket_Mode_Token
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


app = App(token = Slack_Bot_Token)
app_token = Socket_Mode_Token


SENTENCE = {
    'Hi': 'Hi! Welcome to the chatbot that will light up your heart! If you are curious about how to use this chatbot.. type "Explain".',
    'Explain': 'This chatbot is here to provide you with the advice you need! If you are going through a tough time or want to overcome challenges, feel free to ask me for help. I can offer advice on topics such as Life, Love, motivation, happiness, friendship, success, failure, challenge, confidence, and more. *****Here is a tip for enjoying this chatbot: always start the first letter with an uppercase***** If you wish to stop chatting with the bot..just type "Quit".',
    'Life': 'Life is what happens when you are busy making other plans. - John Lennon',
    'Love': 'The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart - Helen Keller',
    'Motivation': 'Believe you can and you arere halfway there. - Theodore Roosevelt',
    'Happiness': 'Happiness is not something ready-made. It comes from your own actions. - Dalai Lama',
    'Friendship': 'A real friend is one who walks in when the rest of the world walks out. - Walter Winchell',
    'Success': 'Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill',
    'Failure': 'Success is stumbling from failure to failure with no loss of enthusiasm. - Winston Churchill',
    'Challenge': 'Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine',
    'Confidence': 'Confidence comes not from always being right but from not fearing to be wrong. - Peter T. Mcintyre',
    'Quit': "Thank you! Feel free to come back anytime, and I'll be more than happy to assist you. Have a joyful time and I look forward to seeing you again!"
}

@app.event("app_mention")
def handle_app_mention_events(body, client, say):

    # Reply to mentions in a thread.
    channel_id = print(body["event"]["channel"])

    print(body.get('event', {}).get('text'))

    messages = body.get('event', {}).get('text')
    #print(message)

    outText = ''
    if ('Hi' in messages):
        outText = SENTENCE['Hi']
    elif ('Explain' in messages):
        outText = SENTENCE['Explain']
    elif ('Life' in messages):
        outText = SENTENCE['Life']
    elif ('Love' in messages):
        outText = SENTENCE['Love']
    elif ('Motivation' in messages):
        outText = SENTENCE['Motivation']
    elif ('Happiness' in messages):
        outText = SENTENCE['Happiness']
    elif ('Friendship' in messages):
        outText = SENTENCE['Friendship']
    elif ('Success' in messages):
        outText = SENTENCE['Success']
    elif ('Failure' in messages):
        outText = SENTENCE['Failure']
    elif ('Challenge' in messages):
        outText = SENTENCE['Challenge']
    elif ('Confidence' in messages):
        outText = SENTENCE['Confidence']
    elif ('Quit' in messages):
        outText = SENTENCE['Quit']
    else:
        out_text = "Sorry, I'm not sure how to respond to that."
        
    client.chat_postMessage(
        channel=body["event"]["channel"],  
        thread_ts_=body["event"]["event_ts"],
        text=f"<@{body['event']['user']}>" + outText,
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()