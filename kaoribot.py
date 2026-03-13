import os
import time
import telebot
import requests
from PIL import Image
from io import BytesIO
import random
import yt_dlp
import wikipedia

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")
GENIUS_KEY = os.getenv("GENIUS_KEY")
OWM_KEY = os.getenv("OPENWEATHER_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

BOT_VERSION = "2.6.2"
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
    except Exception as e:
        print(f"⚠️ Erro: {e}")

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
🌻 KAORI BOT 🌻

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

╭━━🎬 YouTube & Música━━╮
/play → Baixar música
/ytthumb → Thumbnail
/ytinfo → Informações do vídeo
/lyrics → Letra da música
/topchart → Top chart
/spotify → Música Spotify

╭━━🎨 Diversão & Arte━━╮
/anime → Anime aleatório
/meme → Meme aleatório
/quote → Quote aleatória
/merece → Frase motivacional
/cat → Foto de gato
/dog → Foto de cachorro
/stickerpack → Pacote de figurinhas

╭━━🌤 Clima & Astronomia━━╮
/clima → Clima da cidade
/forecast → Previsão do tempo
/sunrise → Nascer do sol
/sunset → Pôr do sol

╭━━🧠 Inteligência Artificial━━╮
/ai → Resposta IA
/chat → Conversa com a Kaori
/story → Criar história
/poema → Criar poema

╭━━🎲 Diversão Rápida━━╮
/8ball → Bola 8
/dice → Jogar dado
/truth → Verdade
/dare → Desafio
/roast → Zoar usuário
/compliment → Elogiar usuário
/joke → Piada
/jokeimg → Piada em imagem
/fact → Fato aleatório

╭━━🖼 Figurinhas━━╮
/fig → Transformar imagem em sticker

╰━━ Versão: {BOT_VERSION} ━━╯
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
# /IMG
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
    except Exception as e:
        safe_send(kaori.send_message, msg.chat.id, f"Erro:\n{e}")

# -------------------------
# /GIF
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
# /FIG (imagem)
# -------------------------
@kaori.message_handler(content_types=['photo'])
def fig(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/input.png", "wb") as f:
            f.write(downloaded)
        img = Image.open("temp/input.png").convert("RGBA")
        img.thumbnail((512,512))
        img.save("temp/sticker.webp","WEBP")
        with open("temp/sticker.webp","rb") as s:
            safe_send(kaori.send_sticker, msg.chat.id, s)
    except Exception as e:
        safe_send(kaori.send_message, msg.chat.id, f"Erro:\n{e}")

# -------------------------
# /PLAY (YouTube)
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        safe_send(kaori.reply_to, msg, "Use:\n/play link ou nome da música")
        return
    status = safe_send(kaori.send_message, msg.chat.id, f"🎧 Procurando: {query}")
    try:
        os.makedirs("music", exist_ok=True)
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "music/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "default_search": "ytsearch",
            "postprocessors": [{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename,"rb") as audio:
            safe_send(kaori.send_audio, msg.chat.id, audio, title=info.get("title"))
    except Exception as e:
        safe_send(kaori.send_message, msg.chat.id, f"Erro ao baixar música:\n{e}")

# -------------------------
# ANTI-CRASH: Resposta padrão
# -------------------------
@kaori.message_handler(func=lambda m: True)
def fallback(msg):
    safe_send(kaori.send_message, msg.chat.id, "Desculpe, não entendi. 😅")

# -------------------------
# RUN
# -------------------------
print(f"🌻 Kaori {BOT_VERSION} iniciada")
kaori.infinity_polling()