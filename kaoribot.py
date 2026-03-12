import telebot
import requests
import random
import time
import yt_dlp
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

start_time = time.time()

# 🌻 MENU
MENU = """
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

👤 Usuário
/start → iniciar bot
/menu → abrir comandos
/info → informações do bot
/id → ver seu ID

⚡ Sistema
/ping → ping em ms
/uptime → tempo online

🔎 Pesquisa
/google texto → pesquisar
/img texto → buscar imagem
/wiki termo → pesquisar na Wikipedia

🎧 Música
/play música ou link

🎲 Diversão
/dado → rolar dado
/moeda → cara ou coroa
/frase → frase aleatória
/emoji → emoji aleatório

🖼 Figurinhas
envie uma imagem

╰━━━━━━━━━━━━━━━━━━━━╯
"""

# 🌻 START
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg,"🌸 Olá! Eu sou a KaoriBot!\nUse /menu para ver os comandos.")

# 🌻 MENU
@bot.message_handler(commands=['menu'])
def menu(msg):
    bot.reply_to(msg, MENU)

# 🌻 ID
@bot.message_handler(commands=['id'])
def userid(msg):
    bot.reply_to(msg,f"🆔 Seu ID: {msg.from_user.id}")

# 🌻 PING
@bot.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    message = bot.reply_to(msg,"🏓 Pong...")
    end = time.time()
    ms = int((end-start)*1000)
    bot.edit_message_text(f"🏓 Pong: {ms}ms",msg.chat.id,message.message_id)

# 🌻 UPTIME
@bot.message_handler(commands=['uptime'])
def uptime(msg):
    uptime = int(time.time()-start_time)
    bot.reply_to(msg,f"⏱ Online há {uptime} segundos")

# 🌻 INFO
@bot.message_handler(commands=['info'])
def info(msg):
    uptime = int(time.time()-start_time)

    texto = f"""
🌸 KaoriBot

Versão: 2.3
Ping: use /ping
Uptime: {uptime} segundos

Criado para diversão e utilidades ✨
"""

    bot.reply_to(msg,texto)

# 🌻 GOOGLE
@bot.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google","")

    link = f"https://www.google.com/search?q={query}"

    bot.reply_to(msg,f"🔎 Resultado:\n{link}")

# 🌻 IMG (PIXABAY)
@bot.message_handler(commands=['img'])
def img(msg):
    query = msg.text.replace("/img","")

    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"

    r = requests.get(url).json()

    if r["hits"]:
        imagem = r["hits"][0]["largeImageURL"]
        bot.send_photo(msg.chat.id,imagem)
    else:
        bot.reply_to(msg,"❌ Nenhuma imagem encontrada")

# 🌻 WIKI
@bot.message_handler(commands=['wiki'])
def wiki(msg):

    termo = msg.text.replace("/wiki","")

    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo}"

    r = requests.get(url).json()

    if "extract" in r:
        bot.reply_to(msg,r["extract"][:800])
    else:
        bot.reply_to(msg,"❌ Não encontrei esse termo.")

# 🌻 DADO
@bot.message_handler(commands=['dado'])
def dado(msg):
    n = random.randint(1,6)
    bot.reply_to(msg,f"🎲 Você tirou: {n}")

# 🌻 MOEDA
@bot.message_handler(commands=['moeda'])
def moeda(msg):
    r = random.choice(["Cara","Coroa"])
    bot.reply_to(msg,f"🪙 Resultado: {r}")

# 🌻 FRASE
@bot.message_handler(commands=['frase'])
def frase(msg):

    frases = [
        "🌸 Continue tentando.",
        "✨ Você consegue.",
        "🌻 Cada dia é uma nova chance.",
        "🔥 Nunca desista.",
        "🌈 Coisas boas estão vindo."
    ]

    bot.reply_to(msg,random.choice(frases))

# 🌻 EMOJI
@bot.message_handler(commands=['emoji'])
def emoji(msg):

    emojis = ["🌸","🌻","✨","🔥","🎧","🎮","🍜","🦊"]

    bot.reply_to(msg,random.choice(emojis))

# 🌻 PLAY
@bot.message_handler(commands=['play'])
def play(msg):

    query = msg.text.replace("/play","")

    bot.reply_to(msg,"🎧 Baixando música...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(f"ytsearch:{query}", download=True)

            entry = info['entries'][0]

            filename = ydl.prepare_filename(entry)

            bot.send_audio(msg.chat.id,open(filename,'rb'),title=entry['title'])

    except Exception as e:

        bot.reply_to(msg,f"⚠️ Erro ao baixar música:\n{e}")

# 🌻 RUN
print("🌸 KaoriBot online!")
bot.infinity_polling()