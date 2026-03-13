import os
import time
import telebot
import requests
import random

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")  # seu token no .env
PIXABAY_KEY = os.getenv("PIXABAY_KEY")

bot = telebot.TeleBot(TOKEN)
start_time = time.time()

# -------------------------
# COMANDOS SIMPLES
# -------------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "💛 Olá! Eu sou a KaoriBot 💛\nUse /menu para ver todos os comandos.")

@bot.message_handler(commands=['ping'])
def ping(message):
    latency = int((time.time() - start_time) * 1000)
    bot.reply_to(message, f"🏓 Pong! Latência: {latency}ms")

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.reply_to(message,
        "💛 Comandos disponíveis:\n"
        "/start – Iniciar o bot\n"
        "/ping – Testar velocidade\n"
        "/menu – Ver este menu\n"
        "/pin – Fixar a última mensagem do chat\n"
        "/unpin – Desafixar mensagens fixadas\n"
        "/anime – Puxar imagem aleatória de anime"
    )

# -------------------------
# PIN / UNPIN
# -------------------------
@bot.message_handler(commands=['pin'])
def pin(message):
    try:
        bot.pin_chat_message(message.chat.id, message.message_id)
        bot.reply_to(message, "💛 Mensagem fixada com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"Erro ao fixar: {e}")

@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message, "💛 Todas as mensagens fixadas foram desafixadas!")
    except Exception as e:
        bot.reply_to(message, f"Erro ao desafixar: {e}")

# -------------------------
# ANIME (PIXABAY)
# -------------------------
@bot.message_handler(commands=['anime'])
def anime(message):
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q=anime&image_type=photo&per_page=50"
    resp = requests.get(url).json()
    if resp['hits']:
        img = random.choice(resp['hits'])['webformatURL']
        bot.send_photo(message.chat.id, img)
    else:
        bot.reply_to(message, "💛 Nenhuma imagem encontrada 😢")

# -------------------------
# INICIAR BOT
# -------------------------
print("KaoriBot online! 💛")
bot.infinity_polling()