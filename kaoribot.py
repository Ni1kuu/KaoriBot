import os
import time
import telebot
import requests

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")  # Token do bot no .env
bot = telebot.TeleBot(TOKEN)

# -------------------------
# INÍCIO DO BOT
# -------------------------
start_time = time.time()  # usado para medir latência rápida

# -------------------------
# COMANDOS
# -------------------------

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "💛 Olá! Eu sou a KaoriBot 💛\nUse /menu para ver todos os comandos.")

# /ping - ping rápido
@bot.message_handler(commands=['ping'])
def ping(message):
    start = time.time()
    msg = bot.send_message(message.chat.id, "🏓 Pingando...")
    end = time.time()
    latency = int((end - start) * 1000)  # em ms
    bot.edit_message_text(f"🏓 Pong! Latência: {latency}ms", message.chat.id, msg.message_id)

# /menu - menu estilizado com blocos
@bot.message_handler(commands=['menu'])
def menu(message):
    menu_text = (
        "╭━━ 💛🌻 MENU KAORI 🌻💛 ━━╮\n\n"
        "💛 ⚙️ SISTEMA:\n"
        "💛 /start – Iniciar o bot\n"
        "💛 /ping – Testar velocidade\n"
        "💛 /menu – Ver este menu\n\n"
        "💛 📌 FIXAR MENSAGENS:\n"
        "💛 /pin – Fixar a última mensagem do chat\n"
        "💛 /unpin – Desafixar mensagens fixadas\n\n"
        "💛 🌸 DIVERSÃO:\n"
        "💛 /waifu – Puxar waifu aleatória de anime\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )
    bot.reply_to(message, menu_text)

# /pin - fixar a última mensagem (bot precisa ser admin)
@bot.message_handler(commands=['pin'])
def pin(message):
    try:
        bot.pin_chat_message(message.chat.id, message.message_id)
        bot.reply_to(message, "💛 Mensagem fixada com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao fixar: {e}")

# /unpin - desafixar mensagens fixadas
@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message, "💛 Todas as mensagens fixadas foram desafixadas!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao desafixar: {e}")

# /waifu - waifu aleatória do waifu.pics
@bot.message_handler(commands=['waifu'])
def anime(message):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/waifu").json()
        img_url = resp['url']
        bot.send_photo(message.chat.id, img_url)
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao buscar waifu: {e}")

# -------------------------
# INICIAR BOT
# -------------------------
print("KaoriBot online! 💛")
bot.infinity_polling()