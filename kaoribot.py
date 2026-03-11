import telebot

TOKEN = "MEU_TOKEN"

bot = telebot.TeleBot(TOKEN)

# comando /start
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🌸 Olá! Eu sou a KaoriBot!\nUse /m para ver os comandos."
    )

# comando /fixar
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