import os
import telebot
import requests
import random
import time
from telebot import types

# ----------------------
# VARIÁVEIS
# ----------------------
TOKEN = os.getenv("BOT_TOKEN")
YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")
REDGIFS_TOKEN = os.getenv("REDGIFS_TOKEN")

bot = telebot.TeleBot(TOKEN)

# ----------------------
# SISTEMAS
# ----------------------
antilink = {}
jogo = {}
colecao_waifus = {}
waifu_atual = {}
avisos = {}

palavras = ["computador","banana","anime","python","telegram",
            "programador","internet","gato","waifu","desenvolvedor"]

# ----------------------
# MENU
# ----------------------
MENU = """
╭━━ 💛🌻 MENU KAORI 🌻💛 ━━╮

💛 ⚙️ SISTEMA
/start
/ping

💛 📌 FIXAR
/pin
/unpin

💛 🌸 WAIFU
/waifu – Waifu SFW
/waifunsfw – Waifu NSFW (privado)
/capturar – Capturar waifu
/minhaswaifus – Sua coleção
/rankwaifu – Ranking
/gifnsfw – GIF NSFW anime (privado)

💛 🎮 DIVERSÃO
/gif – GIF anime (opcional)
/hug
/kiss
/meme
/neko
/anagrama
/8ball
/roll
/coin
/quote
/play – Tocar música do YouTube (SP disponível)

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
/warn
/mute
/unmute

╰━━━━━━━━━━━━━━━━━━━━╯
"""

# ----------------------
# START / MENU / PING
# ----------------------
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, MENU)

@bot.message_handler(commands=['ping'])
def ping(m):
    start_time = time.time()
    msg = bot.reply_to(m,"🏓 Pingando...")
    elapsed = int((time.time() - start_time) * 1000)
    bot.edit_message_text(f"🏓 Pong! {elapsed} ms", m.chat.id, msg.message_id)

# ----------------------
# WAIFU SFW / NSFW
# ----------------------
@bot.message_handler(commands=['waifu','waifunsfw'])
def waifu(m):
    if m.text.startswith("/waifunsfw") and m.chat.type != "private":
        bot.reply_to(m,"🚫 NSFW só no privado!")
        return
    url_api = "https://api.waifu.pics/nsfw/waifu" if m.text.startswith("/waifunsfw") else "https://api.waifu.pics/sfw/waifu"
    try:
        r = requests.get(url_api).json()
        img = r["url"]
        waifu_atual[m.chat.id] = img
        bot.send_photo(m.chat.id,img,caption="💛 Waifu apareceu! Use /capturar")
    except:
        bot.reply_to(m,"💛 Não consegui pegar a waifu!")

# ----------------------
# GIF NSFW RedGIFs
# ----------------------
@bot.message_handler(commands=['gifnsfw'])
def gifnsfw(m):
    if m.chat.type != "private":
        bot.reply_to(m,"🚫 NSFW só no privado!")
        return
    try:
        headers = {"Authorization": f"Bearer {REDGIFS_TOKEN}"}
        r = requests.get("https://api.redgifs.com/v2/gifs/search?search_type=all&query=anime+nsfw&count=50", headers=headers).json()
        gifs = r.get("gifs", [])
        if not gifs:
            bot.reply_to(m,"💛 Não encontrei GIFs NSFW!")
            return
        escolhido = random.choice(gifs)
        link = escolhido["urls"]["hd"] or escolhido["urls"]["sd"]
        bot.send_animation(m.chat.id, link)
    except:
        bot.reply_to(m,"💛 Erro ao buscar GIF NSFW!")

# ----------------------
# CAPTURAR WAIFU
# ----------------------
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
    total = len(colecao_waifus.get(user,[]))
    bot.reply_to(m,f"💛 Você possui {total} waifus!")

@bot.message_handler(commands=['rankwaifu'])
def rank(m):
    ranking = [(user,len(lista)) for user,lista in colecao_waifus.items()]
    ranking.sort(key=lambda x:x[1],reverse=True)
    txt = "🏆 Ranking Waifu\n\n"
    for i,(user,total) in enumerate(ranking[:10],1):
        txt += f"{i}° — {total} waifus\n"
    bot.send_message(m.chat.id,txt)

# ----------------------
# GIF Anime (Giphy)
# ----------------------
@bot.message_handler(commands=['gif'])
def gif(m):
    try:
        args = m.text.split()
        termo = "anime " + " ".join(args[1:]) if len(args)>1 else "anime"
        r = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={termo}&limit=25&rating=pg").json()
        data = r.get("data", [])
        if not data:
            bot.reply_to(m,"💛 Não encontrei GIFs!")
            return
        link = random.choice(data)["images"]["original"]["url"]
        bot.send_animation(m.chat.id, link)
    except:
        bot.reply_to(m,"💛 Erro ao buscar GIF!")

# ----------------------
# DIVERSÃO
# ----------------------
@bot.message_handler(commands=['hug','kiss','neko'])
def animacoes(m):
    cmd = m.text.split()[0][1:]
    url = f"https://api.waifu.pics/sfw/{cmd}"
    try:
        r = requests.get(url).json()
        bot.send_animation(m.chat.id,r["url"])
    except:
        bot.reply_to(m,f"💛 Erro ao buscar {cmd}!")

@bot.message_handler(commands=['meme'])
def meme(m):
    r = requests.get("https://meme-api.com/gimme").json()
    bot.send_photo(m.chat.id,r["url"])

@bot.message_handler(commands=['anagrama'])
def anagrama(m):
    palavra = random.choice(palavras)
    misturada = ''.join(random.sample(palavra,len(palavra)))
    jogo[m.chat.id] = palavra
    bot.send_message(m.chat.id,f"💛 Adivinhe: {misturada}")

@bot.message_handler(func=lambda m: True)
def resposta(m):
    # Resposta anagrama
    if m.chat.id in jogo and m.text.lower() == jogo[m.chat.id]:
        username = getattr(m.from_user,"username",m.from_user.first_name)
        bot.reply_to(m,f"💛 @{username} acertou!")
        del jogo[m.chat.id]
        return
    # Antilink inteligente
    if antilink.get(m.chat.id) and ("http" in m.text or "t.me" in m.text):
        try:
            bot.delete_message(m.chat.id,m.message_id)
            bot.ban_chat_member(m.chat.id,m.from_user.id)
            bot.send_message(m.chat.id,"🚫 Link proibido! Usuário banido.")
        except: pass

# ----------------------
# UTILIDADES
# ----------------------
@bot.message_handler(commands=['roll'])
def roll(m): bot.reply_to(m,f"🎲 {random.randint(1,6)}")
@bot.message_handler(commands=['coin'])
def coin(m): bot.reply_to(m,random.choice(["Cara","Coroa"]))
@bot.message_handler(commands=['8ball'])
def ball(m): bot.reply_to(m,random.choice(["Sim","Não","Talvez","Provavelmente"]))
@bot.message_handler(commands=['quote'])
def quote(m):
    frases = ["🌻 Continue tentando","💛 Nunca desista","✨ Um passo por vez","🔥 Você consegue"]
    bot.reply_to(m,random.choice(frases))
@bot.message_handler(commands=['search'])
def search(m):
    try:
        termo = m.text.split(" ",1)[1]
        bot.send_message(m.chat.id,f"https://www.google.com/search?q={termo.replace(' ','+')}")
    except:
        bot.reply_to(m,"Use /search <termo>")
@bot.message_handler(commands=['avatar'])
def avatar(m):
    photos = bot.get_user_profile_photos(m.from_user.id)
    if photos.total_count>0: bot.send_photo(m.chat.id,photos.photos[0][0].file_id)

# ----------------------
# PIN / UNPIN (privado e grupos)
# ----------------------
@bot.message_handler(commands=['pin'])
def pin(m):
    if m.reply_to_message:
        try:
            bot.pin_chat_message(m.chat.id,m.reply_to_message.message_id)
            bot.reply_to(m,"📌 Mensagem fixada!")
        except:
            bot.reply_to(m,"🚫 Não foi possível fixar!")
    else:
        bot.reply_to(m,"💛 Responda à mensagem que deseja fixar!")

@bot.message_handler(commands=['unpin'])
def unpin(m):
    try:
        bot.unpin_all_chat_messages(m.chat.id)
        bot.reply_to(m,"📌 Todas as mensagens desfixadas!")
    except:
        bot.reply_to(m,"🚫 Não foi possível desfixar!")

# ----------------------
# MODERAÇÃO
# ----------------------
@bot.message_handler(commands=['ban'])
def ban(m):
    if m.reply_to_message:
        bot.ban_chat_member(m.chat.id,m.reply_to_message.from_user.id)

@bot.message_handler(commands=['antilink'])
def anti(m):
    args = m.text.split()
    if len(args)<2: return
    if args[1].lower()=="on": antilink[m.chat.id]=True; bot.reply_to(m,"🚫 Antilink ativado")
    elif args[1].lower()=="off": antilink[m.chat.id]=False; bot.reply_to(m,"✅ Antilink desativado")

# Warn / Mute / Unmute
@bot.message_handler(commands=['warn'])
def warn(m):
    if m.chat.type=="private": bot.reply_to(m,"🚫 Apenas em grupos!"); return
    if not m.reply_to_message: bot.reply_to(m,"💛 Responda a mensagem do usuário."); return
    user = m.reply_to_message.from_user
    chat = m.chat.id
    if chat not in avisos: avisos[chat]={}
    avisos[chat][user.id] = avisos[chat].get(user.id,0)+1
    bot.reply_to(m,f"⚠️ {user.first_name} recebeu um aviso! Total: {avisos[chat][user.id]}")

@bot.message_handler(commands=['mute'])
def mute(m):
    if m.chat.type=="private": bot.reply_to(m,"🚫 Apenas em grupos!"); return
    if not m.reply_to_message: bot.reply_to(m,"💛 Responda a mensagem do usuário."); return
    args = m.text.split()
    minutos = int(args[1]) if len(args)>1 else 10
    user = m.reply_to_message.from_user
    chat = m.chat.id
    bot.restrict_chat_member(chat,user.id,permissions=types.ChatPermissions(can_send_messages=False),
                             until_date=int(time.time())+minutos*60)
    bot.reply_to(m,f"🔇 {user.first_name} silenciado por {minutos} minutos!")

@bot.message_handler(commands=['unmute'])
def unmute(m):
    if m.chat.type=="private": bot.reply_to(m,"🚫 Apenas em grupos!"); return
    if not m.reply_to_message: bot.reply_to(m,"💛 Responda a mensagem do usuário."); return
    user = m.reply_to_message.from_user
    chat = m.chat.id
    bot.restrict_chat_member(chat,user.id,permissions=types.ChatPermissions(can_send_messages=True))
    bot.reply_to(m,f"🔊 {user.first_name} foi desmutado!")

# ----------------------
# CLEAR / CLEARALL
# ----------------------
@bot.message_handler(commands=['clear'])
def clear(m):
    try:
        quantidade = int(m.text.split()[1])
        for i in range(quantidade):
            bot.delete_message(m.chat.id, m.message_id-i)
    except: bot.reply_to(m,"Use /clear <número>")

@bot.message_handler(commands=['clearall'])
def clearall(m):
    try:
        for i in range(100):
            bot.delete_message(m.chat.id, m.message_id-i)
    except: pass

# ----------------------
# PLAY YouTube (SP)
# ----------------------
@bot.message_handler(commands=['play'])
def play(m):
    if m.chat.type=="private": bot.reply_to(m,"🚫 Apenas em grupos!"); return
    args = m.text.split(maxsplit=1)
    if len(args)<2: bot.reply_to(m,"💛 Use /play <nome da música>"); return
    termo = args[1]
    try:
        r = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={termo}&key={YOUTUBE_KEY}&type=video&maxResults=1").json()
        videoId = r['items'][0]['id']['videoId']
        url = f"https://www.youtube.com/watch?v={videoId}"
        bot.send_message(m.chat.id,f"🎵 Tocando: {url}")
    except:
        bot.reply_to(m,"💛 Música não encontrada!")

# ----------------------
# INICIAR BOT
# ----------------------
print("🌻 KaoriBot completo iniciado!")
bot.infinity_polling()