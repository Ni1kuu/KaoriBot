import os
import time
import telebot
import requests
import wikipedia

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")

BOT_VERSION = "2.6.3-mini"
CREATOR = "@ni1ckkj"

start_time = time.time()
kaori = telebot.TeleBot(TOKEN)

# -------------------------
# FUNÇÕES AUXILIARES
# -------------------------
def uptime_str():
    uptime = int(time.time() - start_time)
    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60
    return f"{h}h {m}m {s}s"

def safe_send(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except:
        pass

# -------------------------
# /START
# -------------------------
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = f"Olá {msg.from_user.first_name}! 🌻\nEu sou Kaori, sua assistente. Use /menu para ver os comandos."
    safe_send(kaori.send_message, msg.chat.id, texto)

# -------------------------
# /MENU
# -------------------------
@kaori.message_handler(commands=['menu'])
def menu(msg):
    texto = f"""
🌻 COMANDOS KAORI 🌻

╭━━👤 Usuário━━╮
/start → Iniciar
/info → Informações
/whoami → Quem sou eu
/avatar → Ver avatar

╭━━⚡ Sistema━━╮
/ping → Ping do bot
/clear → Limpar mensagens
/pin → Fixar mensagem
/unpin → Desafixar mensagem

╭━━🔎 Pesquisa━━╮
/google → Pesquisa Google
/img → Buscar imagem
/gif → Buscar gif
/wiki → Buscar Wikipedia
/wikiing → Resumo Wiki
/traduza → Traduzir texto
/shortlink → Encurtar link

╰━━━━━━━━━━━━━━━━━━━━╯
Versão: {BOT_VERSION}
"""
    safe_send(kaori.send_message, msg.chat.id, texto)

# -------------------------
# /INFO
# -------------------------
@kaori.message_handler(commands=['info'])
def info(msg):
    texto = f"""
Kaori {BOT_VERSION}  
Criador: {CREATOR}  
Uptime: {uptime_str()}
"""
    safe_send(kaori.send_message, msg.chat.id, texto)

# -------------------------
# /PING
# -------------------------
@kaori.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    kaori.send_chat_action(msg.chat.id, 'typing')
    elapsed = round((time.time() - start) * 1000)
    safe_send(kaori.send_message, msg.chat.id, f"Pong! {elapsed} ms")

# -------------------------
# /IMG (Pixabay)
# -------------------------
@kaori.message_handler(commands=['img'])
def img(msg):
    query = msg.text.replace("/img", "").strip()
    if not PIXABAY_KEY:
        safe_send(kaori.send_message, msg.chat.id, "❌ API key do Pixabay não configurada")
        return
    if not query:
        safe_send(kaori.reply_to, msg, "Use:\n/img termo")
        return
    try:
        r = requests.get(f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo").json()
        if r['hits']:
            safe_send(kaori.send_photo, msg.chat.id, r['hits'][0]['largeImageURL'])
        else:
            safe_send(kaori.send_message, msg.chat.id, "❌ Nenhuma imagem encontrada")
    except:
        safe_send(kaori.send_message, msg.chat.id, "❌ Erro ao buscar imagem")

# -------------------------
# /GIF (Giphy)
# -------------------------
@kaori.message_handler(commands=['gif'])
def gif(msg):
    query = msg.text.replace("/gif", "").strip()
    if not GIPHY_KEY:
        safe_send(kaori.send_message, msg.chat.id, "❌ API key do Giphy não configurada")
        return
    if not query:
        safe_send(kaori.reply_to, msg, "Use:\n/gif termo")
        return
    try:
        r = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={query}&limit=1&rating=g").json()
        gif_url = r["data"][0]["images"]["original"]["url"]
        safe_send(kaori.send_animation, msg.chat.id, gif_url)
    except:
        safe_send(kaori.send_message, msg.chat.id, "❌ Nenhum gif encontrado")

# -------------------------
# /WIKI
# -------------------------
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    query = msg.text.replace("/wiki","").strip()
    if not query:
        safe_send(kaori.reply_to, msg, "Use:\n/wiki termo")
        return
    try:
        resultado = wikipedia.summary(query, sentences=3, auto_suggest=True)
        safe_send(kaori.send_message, msg.chat.id, resultado)
    except:
        safe_send(kaori.send_message, msg.chat.id, "❌ Nenhum resultado encontrado")

# -------------------------
# ANTI-CRASH
# -------------------------
@kaori.message_handler(func=lambda m: True)
def fallback(msg):
    safe_send(kaori.send_message, msg.chat.id, "Desculpe, não entendi. 😅")

# -------------------------
# RUN
# -------------------------
print(f"🌻 Kaori {BOT_VERSION} iniciada")
kaori.infinity_polling()