import telebot

TOKEN = "8791892359:AAG-b-Nm_S3hKx0Giaq3H4C-RAS1F7xITSU"

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