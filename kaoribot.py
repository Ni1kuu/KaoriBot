import telebot

TOKEN = "8791892359:AAHgDmGvBNBueRDm5vwdZmT9Hjj1_LGhaTI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['fixar'])
def fixar(msg):
    mensagem = bot.send_message(
        msg.chat.id,
        "📌 Mensagem fixada pela Kaori 🌸"
    )
    bot.pin_chat_message(
        msg.chat.id,
        mensagem.message_id
    )

print("Kaori está online 🌸")
bot.infinity_polling()