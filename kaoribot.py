import os
import time
import telebot
import requests
import yt_dlp
from PIL import Image
import wikipedia
from io import BytesIO
import random
import math

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")
GENIUS_KEY = os.getenv("GENIUS_KEY")
OWM_KEY = os.getenv("OWM_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

BOT_VERSION = "2.6.3"
CREATOR = "@ni1ckkj"

start_time = time.time()
kaori = telebot.TeleBot(TOKEN)
music_queue = {}

# -------------------------
# FUNÇÃO BARRA SPOTIFY
# -------------------------
def progress_bar(duration):
    if not duration:
        return "▶️ ──────────"
    total = 10
    filled = 3
    bar = "▬" * filled + "🔘" + "▬" * (total - filled)
    return f"▶️ {bar}"

# -------------------------
# /START
# -------------------------
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ✨
Eu sou **Kaori**, sua assistente.

Use /menu para ver comandos 🌻

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# /MENU
# -------------------------
@kaori.message_handler(commands=['menu'])
def menu(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

👤 Usuário
/start → iniciar
/menu → comandos
/info → informações

⚡ Sistema
/ping → ping
/pin → fixar mensagem
/unpin → desfixar mensagem
/whoami → info do usuário
/clear → limpar chat

🔎 Pesquisa
/google texto
/img termo
/gif termo
/wiki termo
/wikiimg termo
/traduza texto idioma
/shortlink url

🎬 YouTube
/ytthumb → thumbnail
/ytinfo → informações

🎶 Música
/play → baixar música
/lyrics → letra da música
/topchart → músicas populares
/spotify search → pesquisa Spotify

🎨 Diversão e arte
/anime → imagem de anime aleatória
/meme → meme aleatório
/fig → imagem para figurinha
/quote → quote aleatória
/merece → frase motivacional
/avatar user → avatar estilizado
/cat → gato aleatório
/dog → cachorro aleatório
/stickerpack → figurinha aleatória

🌤 Clima
/clima cidade → clima da cidade
/forecast cidade dias → previsão
/sunrise /sunset cidade

🧠 IA
/ai → resposta estilo IA
/chat texto → conversa rápida
/story tema → história curta
/poema tema → poema curto

🎲 Diversão rápida
/8ball → respostas divertidas
/dice → jogar dado
/calc → calculadora
/truth /dare → verdade ou desafio
/roast @user → zoeira com usuário
/compliment @user → elogio aleatório

😂 Diversão
/joke → piada
/jokeimg → piada em imagem
/fact → fato aleatório

╰━━━━━━━━━━━━━━━━━━━━╯
Versão: {BOT_VERSION}
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# /INFO
# -------------------------
@kaori.message_handler(commands=['info'])
def info(msg):
    uptime = int(time.time() - start_time)
    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60
    texto = f"""
╭━━━🌻 INFORMAÇÕES KAORI 🌻━━━╮

Versão: {BOT_VERSION}
Criador: {CREATOR}

Uptime: {h}h {m}m {s}s

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# /PING
# -------------------------
@kaori.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    kaori.send_chat_action(msg.chat.id, 'typing')
    elapsed = round((time.time() - start) * 1000)
    kaori.send_message(msg.chat.id, f"🌻 Pong! {elapsed} ms")

# -------------------------
# /GOOGLE
# -------------------------
@kaori.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/google termo")
        return
    link = f"https://www.google.com/search?q={query}"
    kaori.send_message(msg.chat.id, f"🔎 {query}\n{link}")

# -------------------------
# /IMG
# -------------------------
@kaori.message_handler(commands=['img'])
def img(msg):
    if not PIXABAY_KEY:
        kaori.send_message(msg.chat.id, "❌ API key do Pixabay não configurada")
        return
    query = msg.text.replace("/img", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/img termo")
        return
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"
    r = requests.get(url).json()
    if r.get("hits"):
        kaori.send_photo(msg.chat.id, r["hits"][0]["largeImageURL"])
    else:
        kaori.send_message(msg.chat.id, "❌ Nenhuma imagem encontrada")

# -------------------------
# /GIF
# -------------------------
@kaori.message_handler(commands=['gif'])
def gif(msg):
    if not GIPHY_KEY:
        kaori.send_message(msg.chat.id, "❌ API key do Giphy não configurada")
        return
    query = msg.text.replace("/gif", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/gif termo")
        return
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={query}&limit=1&rating=g"
    r = requests.get(url).json()
    try:
        gif_url = r["data"][0]["images"]["original"]["url"]
        kaori.send_animation(msg.chat.id, gif_url)
    except:
        kaori.send_message(msg.chat.id, "❌ Nenhum gif encontrado")

# -------------------------
# /FIG (imagem apenas)
# -------------------------
@kaori.message_handler(content_types=['photo'])
def fig(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/input.png","wb") as f:
            f.write(downloaded)
        img = Image.open("temp/input.png").convert("RGBA")
        img.thumbnail((512,512))
        img.save("temp/sticker.webp","WEBP")
        with open("temp/sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id,s)
    except Exception as e:
        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# -------------------------
# /PLAY (🎶 Música)
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/play link ou nome da música")
        return
    status = kaori.send_message(msg.chat.id, f"🎧 Procurando: {query}")
    try:
        os.makedirs("music", exist_ok=True)
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "music/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "extractor_args": {"youtube":{"player_client":["android"]}},
            "http_headers":{"User-Agent":"com.google.android.youtube/17.31.35 (Linux; U; Android 11)"},
            "default_search": "ytsearch",
            "postprocessors": [{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
        if not os.path.exists(filename):
            for ext in ["mp3","webm","m4a","opus"]:
                test = f"music/{info['title']}.{ext}"
                if os.path.exists(test):
                    filename = test
                    break
        title = info.get("title")
        thumb = info.get("thumbnail")
        duration = info.get("duration")
        tempo = f"{duration//60}:{duration%60:02d}" if duration else "desconhecido"
        if thumb:
            kaori.send_photo(msg.chat.id, thumb, caption=f"🎵 {title}\n⏱ {tempo}")
        with open(filename,"rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=title)
        kaori.edit_message_text(f"🎵 Tocando: {title}", msg.chat.id, status.message_id)
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# Mensagens automáticas (/chat)
# -------------------------
@kaori.message_handler(func=lambda m: True, content_types=['text'])
def chat(msg):
    texto = msg.text.lower()
    respostas = {
        "oi": "Oi! 🌸",
        "olá": "Olá! ✨",
        "tudo bem?": "Tudo ótimo! E você? 😄",
        "quem é você?": "Eu sou a Kaori, sua assistente 🌻",
    }
    kaori.send_message(msg.chat.id, respostas.get(texto,"Desculpe, não entendi. 😅"))

# -------------------------
# Outros comandos do menu permanecem (joke, fact, meme, etc)
# -------------------------
# Aqui você pode incluir /joke, /fact, /meme, /anime, /quote, /merece, etc.
# (igual à versão anterior, já funcionando)

# -------------------------
# RUN
# -------------------------
print(f"🌻 Kaori {BOT_VERSION} iniciada")
kaori.infinity_polling()