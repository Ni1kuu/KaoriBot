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
# START
# ======================
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,"💛 KaoriBot online!\nUse /menu")

# ======================
# MENU
# ======================
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
    chat_type = m.chat.type  # 'private', 'group', 'supergroup'
    if m.text.startswith("/waifunsfw"):
        if chat_type != "private":
            bot.reply_to(m,"🚫 NSFW só no chat privado!")
            return
        url_api = "https://api.waifu.pics/nsfw/waifu"
    else:
        url_api = "https://api.waifu.pics/sfw/waifu"
    try:
        r = requests.get(url_api)
        data = r.json()
        img = data["images"][0]["url"]
        waifu_atual[m.chat.id] = img
        bot.send_photo(m.chat.id, img, caption="💛 Uma waifu apareceu!\nUse /capturar")
    except:
        bot.reply_to(m,"💛 Não consegui pegar a waifu!")

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
# GIF ANIME via Tenor
# ======================
@bot.message_handler(commands=['gif'])
def gif(m):
    try:
        args = m.text.split()
        if len(args) > 1:
            termo = "anime " + " ".join(args[1:])
        else:
            termo = "anime"
        url = f"https://tenor.googleapis.com/v2/search?q={termo}&key={TENOR_KEY}&limit=20"
        r = requests.get(url).json()
        resultados = r.get("results",[])
        if not resultados:
            bot.reply_to(m,"💛 Não encontrei nenhum gif!")
            return
        gif_escolhido = random.choice(resultados)
        link = gif_escolhido["media_formats"]["gif"]["url"]
        bot.send_animation(m.chat.id, link)
    except:
        bot.reply_to(m,"💛 Erro ao buscar gif!")

# ======================
# HUG / KISS
# ======================
@bot.message_handler(commands=['hug'])
def hug(m):
    r = requests.get("https://api.waifu.pics/sfw/hug").json()
    bot.send_animation(m.chat.id,r["url"])

@bot.message_handler(commands=['kiss'])
def kiss(m):
    r = requests.get("https://api.waifu.pics/sfw/kiss").json()
    bot.send_animation(m.chat.id,r["url"])

# ======================
# MEME
# ======================
@bot.message_handler(commands=['meme'])
def meme(m):
    r = requests.get("https://meme-api.com/gimme").json()
    bot.send_photo(m.chat.id,r["url"])

# ======================
# NEKO
# ======================
@bot.message_handler(commands=['neko'])
def neko(m):
    r = requests.get("https://api.waifu.pics/sfw/neko").json()
    bot.send_photo(m.chat.id,r["url"])

# ======================
# ANAGRAMA
# ======================
@bot.message_handler(commands=['anagrama'])
def anagrama(m):
    palavra = random.choice(palavras)
    misturada = ''.join(random.sample(palavra,len(palavra)))
    jogo[m.chat.id] = palavra
    bot.send_message(m.chat.id,f"💛 Adivinhe: {misturada}")

# ======================
# RESPOSTA ANAGRAMA E ANTILINK
# ======================
@bot.message_handler(func=lambda m: True)
def resposta(m):
    # Anagrama
    if m.chat.id in jogo:
        if m.text.lower() == jogo[m.chat.id]:
            username = getattr(m.from_user,"username",m.from_user.first_name)
            bot.reply_to(m,f"💛 @{username} acertou!")
            del jogo[m.chat.id]
            return
    # Antilink
    if m.chat.id in antilink and antilink[m.chat.id]:
        if m.text and ("http" in m.text or "t.me" in m.text):
            try:
                bot.delete_message(m.chat.id,m.message_id)
                bot.ban_chat_member(m.chat.id,m.from_user.id)
                bot.send_message(m.chat.id,"🚫 Link proibido! Usuário banido.")
            except:
                pass

# ======================
# UTILIDADES
# ======================
@bot.message_handler(commands=['roll'])
def roll(m):
    bot.reply_to(m,f"🎲 {random.randint(1,6)}")

@bot.message_handler(commands=['coin'])
def coin(m):
    bot.reply_to(m,random.choice(["Cara","Coroa"]))

@bot.message_handler(commands=['8ball'])
def ball(m):
    respostas = ["Sim","Não","Talvez","Provavelmente"]
    bot.reply_to(m,random.choice(respostas))

@bot.message_handler(commands=['quote'])
def quote(m):
    frases = [
        "🌻 Continue tentando",
        "💛 Nunca desista",
        "✨ Um passo por vez",
        "🔥 Você consegue"
    ]
    bot.reply_to(m,random.choice(frases))

@bot.message_handler(commands=['search'])
def search(m):
    try:
        termo = m.text.split(" ",1)[1]
        link = termo.replace(" ","+")
        bot.send_message(m.chat.id,f"https://www.google.com/search?q={link}")
    except:
        bot.reply_to(m,"Use /search <termo>")

@bot.message_handler(commands=['avatar'])
def avatar(m):
    photos = bot.get_user_profile_photos(m.from_user.id)
    if photos.total_count > 0:
        bot.send_photo(m.chat.id,photos.photos[0][0].file_id)

# ======================
# PIN / UNPIN
# ======================
@bot.message_handler(commands=['pin'])
def pin(m):
    if m.reply_to_message:
        bot.pin_chat_message(m.chat.id,m.reply_to_message.message_id)

@bot.message_handler(commands=['unpin'])
def unpin(m):
    if m.reply_to_message:
        bot.unpin_chat_message(m.chat.id,m.reply_to_message.message_id)
    else:
        bot.unpin_all_chat_messages(m.chat.id)

# ======================
# BAN
# ======================
@bot.message_handler(commands=['ban'])
def ban(m):
    if m.reply_to_message:
        uid = m.reply_to_message.from_user.id
        bot.ban_chat_member(m.chat.id,uid)

# ======================
# ANTILINK
# ======================
@bot.message_handler(commands=['antilink'])
def anti(m):
    args = m.text.split()
    if len(args)<2: return
    if args[1].lower() == "on":
        antilink[m.chat.id] = True
        bot.reply_to(m,"🚫 Antilink ativado")
    if args[1].lower() == "off":
        antilink[m.chat.id] = False
        bot.reply_to(m,"✅ Antilink desativado")

# ======================
# CLEAR / CLEARALL
# ======================
@bot.message_handler(commands=['clear'])
def clear(m):
    try:
        quantidade = int(m.text.split()[1])
        for i in range(quantidade):
            bot.delete_message(m.chat.id, m.message_id-i)
    except:
        bot.reply_to(m,"Use /clear <número>")

@bot.message_handler(commands=['clearall'])
def clearall(m):
    try:
        for i in range(100):
            bot.delete_message(m.chat.id, m.message_id-i)
    except:
        pass

# ======================
# INICIAR BOT
# ======================
print("🌻 KaoriBot v4.1 iniciada")
bot.infinity_polling()