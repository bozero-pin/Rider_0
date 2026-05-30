import telebot
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is online ✅")

@bot.message_handler(func=lambda m: True)
def anti_links(message):
    if message.text and "t.me/" in message.text.lower():
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "Links are not allowed.")
        except:
            pass

print("Bot running...")
bot.infinity_polling()
