import os
import time
import telebot
import requests
import random

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")  # Coloque o token do bot no Railway Secrets
bot = telebot.TeleBot(TOKEN)

# -------------------------
# COMANDOS PRINCIPAIS
# -------------------------

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "💛 Olá! Eu sou a KaoriBot 💛\nUse /menu para ver todos os comandos.")

# /ping - animado com latência real
@bot.message_handler(commands=['ping'])
def ping(message):
    start = time.time()
    msg = bot.send_message(message.chat.id, "🏓 Pingando 💛🌻")
    
    # animação de pontos
    for i in range(6):
        time.sleep(0.3)
        pontos = '.' * ((i % 3) + 1)
        bot.edit_message_text(f"🏓 Pingando{pontos} 💛🌻", message.chat.id, msg.message_id)
    
    latency = int((time.time() - start) * 1000)
    bot.edit_message_text(f"🏓 Pong! Latência real: {latency}ms 💛🌻", message.chat.id, msg.message_id)

# /menu - menu estilizado atualizado
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
        "💛 /waifu – Puxar waifu aleatória\n"
        "💛 /hug – Enviar abraço em GIF\n"
        "💛 /kiss – Enviar beijo em GIF\n"
        "💛 /meme – Puxar meme aleatório em português\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )
    bot.reply_to(message, menu_text)

# -------------------------
# PIN / UNPIN
# -------------------------
@bot.message_handler(commands=['pin'])
def pin(message):
    try:
        bot.pin_chat_message(message.chat.id, message.message_id)
        bot.reply_to(message, "💛 Mensagem fixada com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao fixar: {e}")

@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message, "💛 Todas as mensagens fixadas foram desafixadas!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao desafixar: {e}")

# -------------------------
# /waifu - waifu aleatória
@bot.message_handler(commands=['waifu'])
def waifu(message):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/waifu").json()
        img_url = resp['url']
        bot.send_photo(message.chat.id, img_url)
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao buscar waifu: {e}")

# -------------------------
# /hug - GIF de abraço
@bot.message_handler(commands=['hug'])
def hug(message):
    hugs = [
        "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
        "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
        "https://media.giphy.com/media/wnsgren9NtITS/giphy.gif"
    ]
    bot.send_animation(message.chat.id, random.choice(hugs))

# /kiss - GIF de beijo
@bot.message_handler(commands=['kiss'])
def kiss(message):
    kisses = [
        "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif",
        "https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif",
        "https://media.giphy.com/media/bGm9FuBCGg4SY/giphy.gif"
    ]
    bot.send_animation(message.chat.id, random.choice(kisses))

# /meme - meme aleatório em português
@bot.message_handler(commands=['meme'])
def meme(message):
    try:
        resp = requests.get("https://meme-api.com/gimme/ptbr").json()
        meme_url = resp['url']
        bot.send_photo(message.chat.id, meme_url)
    except:
        bot.reply_to(message, "💛 Não consegui pegar um meme 😢")

# -------------------------
# INICIAR BOT
print("KaoriBot online! 💛")
bot.infinity_polling()