import os
import telebot
from dotenv import load_dotenv
from Bard import Chatbot

load_dotenv()
token = str(os.getenv("TOKEN"))
bot_token = os.getenv("BOT")
adminId = int(os.getenv("BOT_ADMIN"))

bot = telebot.TeleBot(bot_token)
chatbot = Chatbot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, "<b>Welcome!</b> ✨\n<i>Send any query or ask questions.</i>", parse_mode="HTML")


@bot.message_handler(func=lambda message: True)
def bard(message):
    if message.from_user.id != adminId:
        bot.reply_to(
            message, "<b>You are not authorized to use this bot.</b>", parse_mode="HTML")
        return
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        reply = chatbot.ask(message.text)
        bot.reply_to(message, reply['content'])
    except Exception as e:
        bot.reply_to(message, f"Oops! Something went wrong. {e}")


bot.polling()
