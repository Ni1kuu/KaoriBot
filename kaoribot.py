import os
import telebot
import requests
import random
import time
import urllib.parse
from telebot import types

# ----------------------
# VARIÁVEIS
# ----------------------
TOKEN = os.getenv("BOT_TOKEN")
GIPHY_KEY = os.getenv("GIPHY_KEY")
YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")

bot = telebot.TeleBot(TOKEN)
antilink = {}

start_time = time.time()

MENU = """
╭━━ 💛🌻 MENU HIKARI 🌻💛 ━━╮

💛 ⚙️ SISTEMA
/start – Iniciar Hikari
/ping – Testar ping
/info – Informações do bot

💛 📌 FIXAR
/pin – Fixar mensagem
/unpin – Desfixar mensagens

💛 🌸 WAIFU
/waifu – Waifu SFW
/waifunsfw – Waifu NSFW (privado)

💛 🎮 DIVERSÃO
/gif – GIF anime (opcional)
/meme – Meme em português 🇧🇷
/play – Tocar música do YouTube 🎵

💛 🛠 UTILIDADES
/userinfo – Informações do usuário 👤
/avatar – Avatar do usuário 🖼
/google – Pesquisar no Google 🔎

💛 🛡 MODERAÇÃO
/ban – Banir usuário 🚫
/antilink on/off – Anti-link 🔗

╰━━━━━━━━━━━━━━━━━━━━╯
"""
"""

# ======================
# START / PING
# ======================
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, MENU)

@bot.message_handler(commands=['ping'])
def ping(m):
    start = time.time()
    msg = bot.reply_to(m,"🏓 Pingando...")
    elapsed = int((time.time() - start) * 1000)
    bot.edit_message_text(f"🏓 Pong! {elapsed} ms", m.chat.id, msg.message_id)

# ======================
# INFO
# ======================
@bot.message_handler(commands=['info'])
def info(m):
    uptime = int(time.time() - start_time)
    h = uptime // 3600
    mnt = (uptime % 3600) // 60
    s = uptime % 60
    msg = f"""╭━━━━━━━━━━━━━━━
🌻 INFO HIKARI 🌻
╰━━━━━━━━━━━━━━━
🌻 Versão: 1.0
👤 Criador: @ni1ckkj
⏱ Uptime: {h}h {mnt}m {s}s"""
    bot.send_message(m.chat.id, msg)

# ======================
# PIN / UNPIN
# ======================
@bot.message_handler(commands=['pin'])
def pin(m):
    if m.reply_to_message:
        try:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)
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

# ======================
# WAIFU SFW / NSFW
# ======================
@bot.message_handler(commands=['waifu','waifunsfw'])
def waifu(m):
    if m.text.startswith("/waifunsfw") and m.chat.type != "private":
        bot.reply_to(m,"🚫 NSFW só no privado!")
        return
    url_api = "https://api.waifu.pics/nsfw/waifu" if m.text.startswith("/waifunsfw") else "https://api.waifu.pics/sfw/waifu"
    try:
        r = requests.get(url_api).json()
        bot.send_photo(m.chat.id, r["url"], caption="💛 Aqui está sua waifu!")
    except:
        bot.reply_to(m,"💛 Não consegui pegar a waifu!")

# ======================
# GIF (Giphy)
# ======================
@bot.message_handler(commands=['gif'])
def gif(m):
    try:
        args = m.text.split()
        termo = "anime " + " ".join(args[1:]) if len(args) > 1 else "anime"
        r = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={termo}&limit=25&rating=pg").json()
        data = r.get("data", [])
        if not data:
            bot.reply_to(m,"💛 Não encontrei GIFs nessa categoria!")
            return
        bot.send_animation(m.chat.id, random.choice(data)["images"]["original"]["url"])
    except:
        bot.reply_to(m,"💛 Erro ao buscar GIF!")

# ======================
# MEME
# ======================
@bot.message_handler(commands=['meme'])
def meme(m):
    try:
        r = requests.get("https://meme-api.com/gimme/pt_br").json()
        bot.send_photo(m.chat.id, r['url'])
    except:
        bot.reply_to(m,"💛 Não consegui buscar um meme.")

# ======================
# PLAY (YouTube)
# ======================
@bot.message_handler(commands=['play'])
def play(m):
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(m, "💛 Use: /play <nome da música>")
        return
    query = urllib.parse.quote_plus(args[1])
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_KEY}&maxResults=1&type=video"
        r = requests.get(url).json()
        if not r["items"]:
            bot.reply_to(m,"💛 Música não encontrada!")
            return
        video = r["items"][0]
        titulo = video["snippet"]["title"]
        canal = video["snippet"]["channelTitle"]
        video_id = video["id"]["videoId"]
        link = f"https://youtu.be/{video_id}"
        bot.send_message(m.chat.id, f"🎵 {titulo}\n📺 Canal: {canal}\n▶️ {link}")
    except:
        bot.reply_to(m,"💛 Erro ao buscar música!")

# ======================
# GOOGLE
# ======================
@bot.message_handler(commands=['google'])
def google(m):
    try:
        texto = m.text.replace("/google","").strip()
        if not texto:
            bot.reply_to(m,"💛 Use: /google <termo>")
            return
        termo = urllib.parse.quote_plus(texto)
        link = f"https://www.google.com/search?q={termo}"
        bot.send_message(m.chat.id, f"🔎 Pesquisa Google\n📌 {texto}\n🌐 {link}")
    except:
        bot.reply_to(m,"💛 Erro ao fazer a pesquisa.")

# ======================
# USERINFO (com @)
# ======================
@bot.message_handler(commands=['userinfo'])
def userinfo(m):
    try:
        if m.reply_to_message:
            user = m.reply_to_message.from_user
        elif len(m.text.split())>1 and m.text.split()[1].startswith("@"):
            username = m.text.split()[1][1:]
            chat_members = bot.get_chat_administrators(m.chat.id) + bot.get_chat_members(m.chat.id) if m.chat.type!="private" else []
            user = None
            for member in chat_members:
                if hasattr(member,"user") and member.user.username == username:
                    user = member.user
                    break
            if not user:
                bot.reply_to(m,"💛 Usuário não encontrado no chat.")
                return
        else:
            user = m.from_user
        msg = f"""💛 Informações do usuário:
- Nome: {user.first_name}
- Username: @{user.username if user.username else 'Não possui'}
- ID: {user.id}
- Is bot: {user.is_bot}
"""
        bot.send_message(m.chat.id,msg)
    except:
        bot.reply_to(m,"💛 Erro ao pegar informações.")

# ======================
# AVATAR (com @)
# ======================
@bot.message_handler(commands=['avatar'])
def avatar(m):
    try:
        if m.reply_to_message:
            user = m.reply_to_message.from_user
        elif len(m.text.split())>1 and m.text.split()[1].startswith("@"):
            username = m.text.split()[1][1:]
            chat_members = bot.get_chat_administrators(m.chat.id) + bot.get_chat_members(m.chat.id) if m.chat.type!="private" else []
            user = None
            for member in chat_members:
                if hasattr(member,"user") and member.user.username == username:
                    user = member.user
                    break
            if not user:
                bot.reply_to(m,"💛 Usuário não encontrado no chat.")
                return
        else:
            user = m.from_user
        photos = bot.get_user_profile_photos(user.id)
        if photos.total_count > 0:
            bot.send_photo(m.chat.id, photos.photos[0][0].file_id, caption="Aqui está o avatar ꒰ᐢ. .ᐢ꒱₊˚⊹")
        else:
            bot.reply_to(m,"💛 Usuário não possui foto de perfil.")
    except:
        bot.reply_to(m,"💛 Erro ao pegar avatar.")

# ======================
# BAN
# ======================
@bot.message_handler(commands=['ban'])
def ban(m):
    if m.reply_to_message:
        try:
            bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.reply_to(m,"🚫 Usuário banido com sucesso!")
        except:
            bot.reply_to(m,"💛 Não foi possível banir o usuário.")
    else:
        bot.reply_to(m,"💛 Responda à mensagem da pessoa que deseja banir.")

# ======================
# ANTILINK
# ======================
@bot.message_handler(commands=['antilink'])
def anti(m):
    args = m.text.split()
    if len(args) < 2: return
    if args[1].lower() == "on":
        antilink[m.chat.id] = True
        bot.reply_to(m,"🚫 Antilink ativado")
    elif args[1].lower() == "off":
        antilink[m.chat.id] = False
        bot.reply_to(m,"✅ Antilink desativado")

@bot.message_handler(func=lambda m: True)
def verifica_link(m):
    if antilink.get(m.chat.id) and ("http" in m.text or "t.me" in m.text):
        try:
            bot.delete_message(m.chat.id, m.message_id)
            bot.ban_chat_member(m.chat.id, m.from_user.id)
            bot.send_message(m.chat.id,"🚫 Link proibido! Usuário banido.")
        except: pass

# ======================
# INICIAR BOT
# ======================
print("🌻 Hikari iniciado!")
bot.infinity_polling()