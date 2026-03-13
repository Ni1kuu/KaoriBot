import os
import telebot
import requests
import random
import time

TOKEN = os.getenv("BOT_TOKEN")
GIPHY_KEY = os.getenv("GIPHY_KEY")

bot = telebot.TeleBot(TOKEN)

# ======================
# SISTEMAS
# ======================
antilink = {}
jogo = {}
colecao_waifus = {}
waifu_atual = {}

palavras = [
    "computador","banana","anime","python","telegram",
    "programador","internet","gato","waifu","desenvolvedor"
]

# ======================
# MENU
# ======================
MENU = """
╭━━ 💛🌻 MENU KAORI 🌻💛 ━━╮

💛 ⚙️ SISTEMA
/start
/ping
/menu

💛 📌 FIXAR
/pin
/unpin

💛 🌸 WAIFU
/waifu – Encontrar waifu SFW
/waifunsfw – Encontrar waifu NSFW (privado)
/capturar – Capturar waifu
/minhaswaifus – Ver coleção
/rankwaifu – Ranking

💛 🎮 DIVERSÃO
/gif – GIF anime (categoria opcional)
/gifnsfw – GIF NSFW anime (privado)
/hug
/kiss
/meme
/neko
/anagrama
/8ball
/roll
/coin
/quote

💛 🛠 UTILIDADES
/userinfo
/chatinfo
/avatar
/say
/search

💛 🛡 MODERAÇÃO
/clear
/clearall
/antilink on/off
/ban

╰━━━━━━━━━━━━━━━━━━━━╯
"""

# ======================
# START / MENU
# ======================
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,"💛 KaoriBot online!\nUse /menu")

@bot.message_handler(commands=['menu'])
def menu(m):
    bot.send_message(m.chat.id, MENU)

# ======================
# PING
# ======================
@bot.message_handler(commands=['ping'])
def ping(m):
    start_time = time.time()
    msg = bot.reply_to(m,"🏓 Pingando...")
    elapsed = int((time.time() - start_time) * 1000)
    bot.edit_message_text(f"🏓 Pong! {elapsed} ms", m.chat.id, msg.message_id)

# ======================
# WAIFU SFW / NSFW
# ======================
@bot.message_handler(commands=['waifu','waifunsfw'])
def waifu(m):
    chat_type = m.chat.type

    if m.text.startswith("/waifunsfw"):
        if chat_type != "private":
            bot.reply_to(m,"🚫 NSFW só no chat privado!")
            return
        url_api = "https://api.waifu.pics/nsfw/waifu"
    else:
        url_api = "https://api.waifu.pics/sfw/waifu"

    try:
        r = requests.get(url_api).json()
        img = r["url"]
        waifu_atual[m.chat.id] = img
        bot.send_photo(m.chat.id, img, caption="💛 Uma waifu apareceu!\nUse /capturar")
    except:
        bot.reply_to(m,"💛 Não consegui pegar a waifu!")

# ======================
# CAPTURAR / MINHAS / RANK
# ======================
@bot.message_handler(commands=['capturar'])
def capturar(m):
    chat = m.chat.id
    user = m.from_user.id
    if chat not in waifu_atual:
        bot.reply_to(m,"💛 Não há waifu para capturar!")
        return
    img = waifu_atual[chat]
    if user not in colecao_waifus:
        colecao_waifus[user] = []
    colecao_waifus[user].append(img)
    bot.reply_to(m,"🌸 Waifu capturada!")

@bot.message_handler(commands=['minhaswaifus'])
def minhas(m):
    user = m.from_user.id
    if user not in colecao_waifus:
        bot.reply_to(m,"💛 Você não tem waifus!")
        return
    total = len(colecao_waifus[user])
    bot.reply_to(m,f"💛 Você possui {total} waifus!")

@bot.message_handler(commands=['rankwaifu'])
def rank(m):
    ranking = [(user,len(lista)) for user,lista in colecao_waifus.items()]
    ranking.sort(key=lambda x:x[1],reverse=True)
    txt = "🏆 Ranking Waifu\n\n"
    for i,(user,total) in enumerate(ranking[:10],1):
        txt += f"{i}° — {total} waifus\n"
    bot.send_message(m.chat.id,txt)

# ======================
# GIF / GIFNSFW (Giphy)
# ======================
def buscar_gif(term, nsfw=False):
    rating = "r" if nsfw else "pg"
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={term}&limit=25&rating={rating}"
    r = requests.get(url).json()
    resultados = r.get("data",[])
    if not resultados:
        return None
    escolhido = random.choice(resultados)
    return escolhido["images"]["original"]["url"]

@bot.message_handler(commands=['gif'])
def gif(m):
    args = m.text.split()
    termo = "anime"
    if len(args) > 1:
        termo += " " + " ".join(args[1:])
    link = buscar_gif(termo)
    if link:
        bot.send_animation(m.chat.id, link)
    else:
        bot.reply_to(m,"💛 Não encontrei GIFs!")

@bot.message_handler(commands=['gifnsfw'])
def gifnsfw(m):
    if m.chat.type != "private":
        bot.reply_to(m,"🚫 NSFW só no chat privado!")
        return
    args = m.text.split()
    termo = "anime"
    if len(args) > 1:
        termo += " " + " ".join(args[1:])
    link = buscar_gif(termo, nsfw=True)
    if link:
        bot.send_animation(m.chat.id, link)
    else:
        bot.reply_to(m,"💛 Não encontrei GIFs NSFW!")

# ======================
# HUG / KISS / NEKO / MEME
# ======================
@bot.message_handler(commands=['hug'])
def hug(m):
    r = requests.get("https://api.waifu.pics/sfw/hug").json()
    bot.send_animation(m.chat.id,r["url"])

@bot.message_handler(commands=['kiss'])
def kiss(m):
    r = requests.get("https://api.waifu.pics/sfw/kiss").json()
    bot.send_animation(m.chat.id,r["url"])

@bot.message_handler(commands=['meme'])
def meme(m):
    r = requests.get("https://meme-api