import os
import telebot
import requests
import random
import time
import re

TOKEN = os.getenv("BOT_TOKEN")
GIPHY_KEY = os.getenv("GIPHY_KEY")

bot = telebot.TeleBot(TOKEN)

antilink = {}
jogo = {}
colecao_waifus = {}
waifu_atual = {}

palavras = [
"computador","banana","anime","python","telegram",
"programador","internet","gato","waifu","desenvolvedor"
]

MENU = """
╭━━ 💛🌻 MENU KAORI 🌻💛 ━━╮

⚙️ SISTEMA
/start
/ping
/menu

🎵 MÚSICA
/play <nome da música>

🌸 WAIFU
/waifu
/waifunsfw
/capturar
/minhaswaifus
/rankwaifu

🎮 DIVERSÃO
/gif
/gifnsfw
/hug
/kiss
/meme
/neko
/anagrama
/8ball
/roll
/coin
/quote

🛠 UTILIDADES
/avatar
/search

🛡 MODERAÇÃO
/clear
/antilink on/off
/ban
"""

# START
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,"💛 KaoriBot online!\nUse /menu")

# MENU
@bot.message_handler(commands=['menu'])
def menu(m):
    bot.send_message(m.chat.id, MENU)

# PING
@bot.message_handler(commands=['ping'])
def ping(m):
    start = time.time()
    msg = bot.reply_to(m,"🏓 Pingando...")
    delay = int((time.time() - start)*1000)
    bot.edit_message_text(f"🏓 Pong {delay} ms",m.chat.id,msg.message_id)

# PLAY
@bot.message_handler(commands=['play'])
def play(m):

    args = m.text.split(" ",1)

    if len(args) < 2:
        bot.reply_to(m,"🎵 Use:\n/play nome da música")
        return

    query = args[1].replace(" ","+")

    url = f"https://www.youtube.com/results?search_query={query}"

    html = requests.get(url).text

    video_ids = re.findall(r"watch\?v=(\S{11})", html)

    if not video_ids:
        bot.reply_to(m,"💛 Não encontrei essa música!")
        return

    link = f"https://www.youtube.com/watch?v={video_ids[0]}"

    bot.send_message(m.chat.id,f"🎵 Resultado:\n{link}")

# WAIFU
@bot.message_handler(commands=['waifu','waifunsfw'])
def waifu(m):

    if m.text.startswith("/waifunsfw") and m.chat.type != "private":
        bot.reply_to(m,"🚫 NSFW só no privado")
        return

    url = "https://api.waifu.pics/sfw/waifu"

    if m.text.startswith("/waifunsfw"):
        url = "https://api.waifu.pics/nsfw/waifu"

    data = requests.get(url).json()

    img = data["url"]

    waifu_atual[m.chat.id] = img

    bot.send_photo(m.chat.id,img,caption="💛 Uma waifu apareceu!\nUse /capturar")

# CAPTURAR
@bot.message_handler(commands=['capturar'])
def capturar(m):

    chat = m.chat.id
    user = m.from_user.id

    if chat not in waifu_atual:
        bot.reply_to(m,"💛 Nenhuma waifu!")
        return

    if user not in colecao_waifus:
        colecao_waifus[user] = []

    colecao_waifus[user].append(waifu_atual[chat])

    bot.reply_to(m,"🌸 Waifu capturada!")

# MINHAS WAIFUS
@bot.message_handler(commands=['minhaswaifus'])
def minhas(m):

    user = m.from_user.id

    if user not in colecao_waifus:
        bot.reply_to(m,"💛 Você não tem waifus")
        return

    bot.reply_to(m,f"💛 Você possui {len(colecao_waifus[user])} waifus")

# GIF
@bot.message_handler(commands=['gif'])
def gif(m):

    termo = "anime"

    args = m.text.split()

    if len(args) > 1:
        termo += " " + " ".join(args[1:])

    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={termo}&limit=25"

    r = requests.get(url).json()

    gifs = r["data"]

    if not gifs:
        bot.reply_to(m,"💛 Não achei gif!")
        return

    gif = random.choice(gifs)

    bot.send_animation(m.chat.id,gif["images"]["original"]["url"])

# ======================
# GIF NSFW (REAL)
# ======================
@bot.message_handler(commands=['gifnsfw'])
def gifnsfw(m):

    if m.chat.type != "private":
        bot.reply_to(m,"🚫 Conteúdo NSFW apenas no privado.")
        return

    try:

        apis = [
            "https://nekos.life/api/v2/img/Random_hentai_gif",
            "https://nekos.life/api/v2/img/pussy",
            "https://nekos.life/api/v2/img/lesbian"
        ]

        url_api = random.choice(apis)

        r = requests.get(url_api).json()

        gif = r["url"]

        bot.send_animation(
            m.chat.id,
            gif,
            caption="🔞 GIF NSFW"
        )

    except Exception as e:
        print("Erro gifnsfw:", e)
        bot.reply_to(m,"💛 Não consegui buscar GIF.")

# HUG
@bot.message_handler(commands=['hug'])
def hug(m):

    r = requests.get("https://api.waifu.pics/sfw/hug").json()

    bot.send_animation(m.chat.id,r["url"])

# KISS
@bot.message_handler(commands=['kiss'])
def kiss(m):

    r = requests.get("https://api.waifu.pics/sfw/kiss").json()

    bot.send_animation(m.chat.id,r["url"])

# MEME
@bot.message_handler(commands=['meme'])
def meme(m):

    r = requests.get("https://meme-api.com/gimme").json()

    bot.send_photo(m.chat.id,r["url"])

# NEKO
@bot.message_handler(commands=['neko'])
def neko(m):

    r = requests.get("https://api.waifu.pics/sfw/neko").json()

    bot.send_photo(m.chat.id,r["url"])

# ANAGRAMA
@bot.message_handler(commands=['anagrama'])
def anagrama(m):

    palavra = random.choice(palavras)

    misturada = ''.join(random.sample(palavra,len(palavra)))

    jogo[m.chat.id] = palavra

    bot.send_message(m.chat.id,f"💛 Adivinhe: {misturada}")

# RESPOSTA
@bot.message_handler(func=lambda m: True)
def resposta(m):

    if m.chat.id in jogo:

        if m.text.lower() == jogo[m.chat.id]:

            bot.reply_to(m,"🎉 Acertou!")

            del jogo[m.chat.id]

# ROLL
@bot.message_handler(commands=['roll'])
def roll(m):
    bot.reply_to(m,f"🎲 {random.randint(1,6)}")

# COIN
@bot.message_handler(commands=['coin'])
def coin(m):
    bot.reply_to(m,random.choice(["Cara","Coroa"]))

# 8BALL
@bot.message_handler(commands=['8ball'])
def ball(m):

    respostas = ["Sim","Não","Talvez","Provavelmente"]

    bot.reply_to(m,random.choice(respostas))

# QUOTE
@bot.message_handler(commands=['quote'])
def quote(m):

    frases = [
    "🌻 Continue tentando",
    "💛 Nunca desista",
    "✨ Um passo por vez",
    "🔥 Você consegue"
    ]

    bot.reply_to(m,random.choice(frases))

# SEARCH
@bot.message_handler(commands=['search'])
def search(m):

    try:
        termo = m.text.split(" ",1)[1]
        link = termo.replace(" ","+")
        bot.send_message(m.chat.id,f"https://google.com/search?q={link}")
    except:
        bot.reply_to(m,"Use /search termo")

# AVATAR
@bot.message_handler(commands=['avatar'])
def avatar(m):

    fotos = bot.get_user_profile_photos(m.from_user.id)

    if fotos.total_count > 0:
        bot.send_photo(m.chat.id,fotos.photos[0][0].file_id)

print("🌻 KaoriBot iniciado")

bot.infinity_polling()