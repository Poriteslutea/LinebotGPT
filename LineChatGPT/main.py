
from flask import Flask,request,abort
import os
from chatgpt import ChatGPT
from questions import get_question

# connet to db
import psycopg2 as db
conn = db.connect(host='localhost', dbname='flaskdb', user='megoo', password=os.getenv("DATABASE_PASSWORD"))


#待官方 API  出來前暫時棄用
# import openai
# openai.api_key = ""
# # my_api_key = "
# 載入 LINE Message API 相關函式庫


from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, PostbackAction,URIAction, MessageAction, FlexSendMessage, ButtonsTemplate



# 新增 TOKEN 進去
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"


# from revChatGPT.Official import Chatbot
# https://github.com/acheong08/ChatGPT/wiki/Setup

# chatbot = Chatbot(api_key=my_api_key)


app = Flask(__name__)

chatgpt = ChatGPT()
# run_with_ngrok(app)   #starts ngrok when the app is run
@app.route("/")
def home():
    return "<h1>Running Flask on Google Colab hihihi! add env!</h1>"
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'






@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    # 分出大類別，回傳Flex Message選單
    if event.message.text == "Python面試題":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,FlexSendMessage(
                alt_text='hello',
                contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://media-cdn.tripadvisor.com/media/attractions-splice-spp-720x480/0f/01/f2/a7.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                    "type": "uri",
                    "uri": "http://linecorp.com/"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "Python面試題",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xl",
                        "spacing": "sm",
                        "contents": []
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "基礎題",
                            "text": "__Python基礎題"
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "進階題",
                            "text": "__Python進階題"
                            }
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "資料庫相關",
                            "text": "__資料庫相關"
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "爬蟲",
                            "text": "__爬蟲"
                            }
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "數據分析",
                            "text": "__數據分析"
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "機器學習",
                            "text": "__機器學習"
                            }
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "資料結構與演算法",
                            "text": "__資料結構與演算法"
                            }
                        }
                        ]
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "新增其他題目",
                        "text": "還沒有這個功能喔哈哈哈"
                        },
                        "gravity": "center",
                        "position": "relative",
                        "offsetBottom": "10%"
                    }
                    ],
                    "backgroundColor": "#ebe8e4"
                }
                }
            ))
        return
    
    if event.message.text.startswith('__'):
        working_status = True
        cata = event.message.text[2:]
        ques = get_question(cata)
        post_ques = '//' + ques
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='question',
                contents={
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": ques,
                            "wrap": True,
                        }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                "type": "postback",
                                "label": "我要問GPT",
                                "data": post_ques,
                                "displayText": "我要求救~"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "換一題",
                                "text": event.message.text
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "回到主頁",
                                "text": "Python面試題"
                                }
                            }
                            ]
                    }
                    }
            )
        )


    if event.message.text == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
        return
    
    if event.message.text == "你是誰":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我是隻聰明的紅毛猩猩！"))
        return

    if event.message.text == "我想跟猩猩閒聊":
        working_status = True

    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))


@line_handler.add(PostbackEvent)
def handle_postback(event):
    res = event.postback.data
    if res.startswith('//'):
        q = res[2:]
        print(q)
        chatgpt.add_msg(f"HUMAN:Python中，{q}\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        # chatgpt.add_msg(f"AI:{reply_msg}\n")
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))
  

if __name__ == "__main__":
  app.run()
  