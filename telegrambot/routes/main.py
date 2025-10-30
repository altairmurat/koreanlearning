import telebot
from telebot import types
from fastapi import HTTPException
from utils.openai_helpers import chat_helper
import logging
import asyncio

bot = telebot.TeleBot('8197697361:AAFNA4kpGc0dsnDCVtisXcVP0-_kqLINI2Q')
logger = logging.getLogger(__name__)
user_level = 0

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("A1-A2", callback_data="A1-A2")
    bt2 = types.InlineKeyboardButton("B1", callback_data="B1")
    markup.row(bt1,bt2)
    bot.send_message(message.chat.id, "Choose your level", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_level(callback):
    user_level = callback.data
    if callback.data == "A1-A2":
        markup = types.InlineKeyboardMarkup()
        bt4 = types.InlineKeyboardButton('5 new korean words', callback_data="words")
        bt5 = types.InlineKeyboardButton('new grammar structure', callback_data="grammar")
        bt6 = types.InlineKeyboardButton('talk with Korean Bot as a real conversation', callback_data="conversation")
        markup.row(bt4)
        markup.row(bt5)
        markup.row(bt6)
        bot.send_message(callback.message.chat.id, f"What do you want to do today with your {user_level} level", reply_markup=markup)
    elif callback.data == "B1":
        markup = types.InlineKeyboardMarkup()
        bt4 = types.InlineKeyboardButton('5 new korean words', callback_data="words")
        bt5 = types.InlineKeyboardButton('new grammar structure', callback_data="grammar")
        bt6 = types.InlineKeyboardButton('talk with Korean Bot as a real conversation', callback_data="conversation")
        markup.row(bt4)
        markup.row(bt5)
        markup.row(bt6)
        bot.send_message(callback.message.chat.id, f"What do you want to do today with your {user_level} level", reply_markup=markup)
    elif callback.data == "words":
        sendingmessage = {"role": "user", "content": f"write me 5 new words please for {user_level} level"}
        try:
            result = asyncio.run(chat_helper(sendingmessage))
            final_result = result.get("content") if isinstance(result, dict) else str(result)
            bot.send_message(callback.message.chat.id, final_result)
        except Exception as e:
            logger.error(e)
            bot.send_message(callback.message.chat.id, f"Error while processing your message.")
    elif callback.data == "grammar":
        sendingmessage = {"role": "user", "content": f"teach me for a new grammar stracture for {user_level} level"}
        try:
            result = asyncio.run(chat_helper(sendingmessage))
            final_result = result.get("content") if isinstance(result, dict) else str(result)
            bot.send_message(callback.message.chat.id, final_result)
        except Exception as e:
            logger.error(e)
            bot.send_message(callback.message.chat.id, f"Error while processing your message.")
    elif callback.data == "conversation":
        sendingmessage = {"role": "user", "content": f"you are a friendly bot that speaks on korean using everything from {user_level} level korean with a user who texts you."}
        try:
            result = asyncio.run(chat_helper(sendingmessage))
            final_result = result.get("content") if isinstance(result, dict) else str(result)
            bot.send_message(callback.message.chat.id, final_result)
        except Exception as e:
            logger.error(e)
            bot.send_message(callback.message.chat.id, f"Error while processing your message.")
    else:
        bot.send_message(callback.message.chat.id, "Error while processing your message.")

@bot.message_handler(content_types=['text'])
def get_username(message):
    global user_level
    sendingmessage = {"role": "user", "content": message.text}
    try:
        result = asyncio.run(chat_helper(sendingmessage))
        final_result = result.get("content") if isinstance(result, dict) else str(result)
        bot.send_message(message.chat.id, final_result)
    except Exception as e:
        logger.error(e)
        bot.send_message(message.chat.id, "Error while processing your message.")

bot.infinity_polling()