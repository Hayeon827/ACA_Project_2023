import logging
import os
import random
import re
import sys

from revChatGPT.V3 import Chatbot

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.error import BoltUnhandledRequestError

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN= #Insert your token here!
SLACK_SIGNING_SECRET= #Insert your signing secret here!

Advice_App = App(token=SLACK_BOT_TOKEN, raise_error_for_unhandled_request=True)

logging.basicConfig(level=logging.INFO)
load_dotenv()

ChatGPTConfig = {
    'api_key': #Insert your api key for ChatGPT
}

if os.getenv("OPENAI_ENGINE"):
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")

chatbot = Chatbot(**ChatGPTConfig)


advice_keywords = ["life", "love", "motivation", "happiness", "friendship", "success", "failure", "challenge", "confidence"]


@Advice_App.event("message")
def handle_message_events(event, message, say):
    user_id = message['user']

    body_text = message["text"].lower()

    if (body_text == '#explain'):
        bot_explain(message, say)

    elif (body_text == '#advice'):
        bot_advice(message, say)

    elif (body_text in advice_keywords):
        print_advice_randome(message, say)

    elif (body_text[0:4] == '#gpt'):
        handle_gpt(event, say)


def bot_explain(message, say):

    guide = [
        "   `#advice`        - Enjoy the light that you need.:hugging_face:",
        "   `#gpt`             - Experince ChatGpt. i.g> #gpt <User_sentence>:face_with_monocle:",
    ]

    guide_list = "\n".join(guide)
    say("This chatbot is here to provide you with the advice you need!\n"
        "If you are having a tough time or want to overcome challenges, feel free to ask me for help.\n\n" + guide_list)


def bot_advice(message, say):

    user_id = message["user"]
    advice = message["text"].lower()

    str_guide = "Type one of below keywords!!\n"
    str_guide += "Life, Love, Motivation, Happiness, Friendship, Success, Failure, Challenge, Confidence\n"

    say(str_guide)


def print_advice_static(message, say):

    user_id = message["user"]
    advice = message["text"].lower()

    if advice in advice_keywords:
        advice_links = {
            'life': 'Life is what happens when you are busy making other plans. - John Lennon',
            'love': 'The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart - Helen Keller',
            'motivation': 'Believe you can and you arere halfway there. - Theodore Roosevelt',
            'happiness': 'Happiness is not something ready-made. It comes from your own actions. - Dalai Lama',
            'friendship': 'A real friend is one who walks in when the rest of the world walks out. - Walter Winchell',
            'success': 'Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill',
            'failure': 'Success is stumbling from failure to failure with no loss of enthusiasm. - Winston Churchill',
            'challenge': 'Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine',
            'confidence': 'Confidence comes not from always being right but from not fearing to be wrong. - Peter T. Mcintyre',
        }
        give_str = advice_links[advice]
        say(f"Here is advice for <{advice}> : {give_str}\n")

    else:
        say("Please type correctly!!")


def print_advice_randome(message, say):

    user_id = message["user"]
    advice = message["text"].lower()

    if advice in advice_keywords:
        advice_links = {
            'life': [':bulb:Life is what happens when you are busy making other plans. - John Lennon',
                    ':bulb:In three words I can sum up everything I have learned about life: it goes on.- Robert Frost',
                    ':bulb:ife is really simple, but we insist on making it complicated. - Confucius',
                    ':bulb:Life is nott about finding yourself. It is about creating yourself. - George Bernard Shaw',
                    ':bulb:The purpose of our lives is to be happy. - Dalai Lama'
                     ],
            'love': [':hearts:The best thing to hold onto in life is each other. - Audrey Hepburn',
                    ':hearts:Love is not something you find. Love is something that finds you. - Loretta Young',
                    ':hearts:The greatest happiness of life is the conviction that we are loved; loved for ourselves, or rather, loved in spite of ourselves. - Victor Hugo',
                    ':hearts:Love is an endless act of forgiveness. Forgiveness is an endless act of love. - Beyoncé',
                    ':hearts:To love oneself is the beginning of a lifelong romance. - Oscar Wilde'
                     ],
            'motivation': [':seedling:The only way to do great work is to love what you do. - Steve Jobs',
                            ':seedling:Believe you can and you are halfway there." - Theodore Roosevelt',
                            ':seedling:Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill',
                            ':seedling:The future depends on what you do today." - Mahatma Gandhi',
                            ':seedling:Your time is limited, do not waste it living life of others. - Steve Jobs',
                            ],
            'happiness': [':blush:Happiness is not something ready-made. It comes from your own actions. - Dalai Lama',
                            ':blush:The happiest people do not have the best of everything, they make the best of everything. - Unknown',
                            ':blush:Happiness is a direction, not a place. - Sydney J. Harris',
                            ':blush:The secret of happiness is not in doing what one likes, but in liking what one does." - James M. Barrie',
                            ':blush:The purpose of our lives is to be happy. - Aristotle'
                            ],
            'friendship': [':people_hugging:A real friend is one who walks in when the rest of the world walks out. - Walter Winchell',
                            ':people_hugging:Friendship is born at that moment when one person says to another, What! You too? I thought I was the only one. - C.S. Lewis',
                            ':people_hugging:Friendship is the only cement that will ever hold the world together. - Woodrow Wilson',
                            ':people_hugging:A friend is someone who knows all about you and still loves you. - Elbert Hubbard',
                            ':people_hugging:The language of friendship is not words but meanings. - Henry David Thoreau',  
                            ],
            'success': [':cherry_blossom:Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. - Albert Schweitzer',
                        ':cherry_blossom:Success is walking from failure to failure with no loss of enthusiasm. - Winston Churchill',
                        ':cherry_blossom:The only place where success comes before work is in the dictionary. - Vidal Sassoon',
                        ':cherry_blossom:Success is to be measured not so much by the position that one has reached in life as by the obstacles which he has overcome. - Booker T. Washington',
                        ':cherry_blossom:Success is not in what you have, but who you are. - Bo Bennett                     '
                        ],
            'failure': [':mending_heart:Success is stumbling from failure to failure with no loss of enthusiasm. - Winston Churchill',
                        ':mending_heart:Failure is simply the opportunity to begin again, this time more intelligently. - Henry Ford',
                        ':mending_heart:Don not be afraid to fail. Be afraid not to try. - Michael Jordan',
                        ':mending_heart:Failure is the condiment that gives success its flavor. - Truman Capote',
                        ':mending_heart:The only real failure is the failure to try, and the measure of success is how we cope with disappointment. - Deborah Moggach'               
                        ],
            'challenge': [':checkered_flag:Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine',
                        ':checkered_flag:The only way to achieve the impossible is to believe it is possible. - Charles Kingsleigh (Alice in Wonderland)',
                        ':checkered_flag:In the middle of every difficulty lies opportunity. - Albert Einstein',
                        ':checkered_flag:When we least expect it, life sets us a challenge to test our courage and willingness to change. - Paulo Coelho',
                        ':checkered_flag:Challenges are gifts that force us to search for a new center of gravity. Don nott fight them. Just find a different way to stand. - Oprah Winfrey'                
                        ],
            'confidence': [':star:Confidence comes not from always being right, but from not fearing to be wrong. - Peter T. Mcintyre'
                            ':star:You yourself, as much as anybody in the entire universe, deserve your love and affection." - Buddha',
                            ':star:With confidence, you have won before you have started. - Marcus Garvey',
                            ':star:The best way to gain self-confidence is to do what you are afraid to do. - Swati Sharma',
                            ':star:To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson   '                
                            ],

        }
        say(random.choice(advice_links[advice]))

    else:
        say("Please type correctly!!")


def handle_gpt(event, say):
    query_str = re.sub("\\s<@[^, ]*|^<@[^, ]*", "", event["text"])
    query_str = query_str[5:]

    print(query_str)
    try:

        user_id = event['user']
        response_message = chatbot.ask(query_str)
        response_message =  f'<@{user_id}> ' + response_message
    except Exception as e:
        print(e, file=sys.stderr)
        response_message = e 

    say(text=response_message)


@Advice_App.event("member_joined_channel")
def welcome_join(event, say):

    user_id = event["user"]
    channel_id = event["channel"]

    welcome_str = f"Nice to Join, <@{user_id}> !!! .\nEnjoy Advice Bot with the command `#explain`."

    say(text=welcome_str, channel=channel_id)


@Advice_App.error
def handle_errors(error) :
    return None


if __name__ == "__main__":
    handler = SocketModeHandler(Advice_App, SLACK_APP_TOKEN)
    handler.start()