import os
import time
import telebot
import requests
import yt_dlp
from PIL import Image
import wikipedia
from io import BytesIO
import random

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")
BOT_VERSION = "2.4.1"
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

🔎 Pesquisa
/google texto → pesquisa Google
/img keyword → imagem
/wiki termo → resumo Wikipedia

🎬 YouTube
/yt → baixar vídeo
/play → baixar música
/ytthumb → thumbnail
/ytinfo → informações

🎶 Música
/lyrics → letra da música

🎨 Diversão e Arte
/anime → imagem de anime aleatória
/meme → meme aleatório (em português)
/gif keyword → gif aleatório
/jokeimg → piada em imagem

🌤 Clima
/clima cidade → clima da cidade

🧠 IA
/ai → resposta estilo IA
/quote → citação motivacional
/8ball pergunta → bola 8 mágica
/dice → joga dado
/calc expressão → calculadora rápida

🖼 Figurinhas
envie imagem → gera figurinha
/envgif → gera figurinha GIF animada

😂 Diversão
/joke → piada texto
/fact → fato curioso
/merece → fato/quote
╰━━━━━━━━━━━━━━━━━━━━╯
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
# GOOGLE
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
# PIXABAY
# -------------------------
@kaori.message_handler(commands=['img'])
def img(msg):
    query = msg.text.replace("/img", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/img termo")
        return
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"
    r = requests.get(url).json()
    if r.get("hits"):
        kaori.send_photo(msg.chat.id, r["hits"][0]["largeImageURL"])
    else:
        kaori.send_message(msg.chat.id, "❌ Nenhuma imagem encontrada.")

# -------------------------
# WIKI
# -------------------------
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    query = msg.text.replace("/wiki", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/wiki termo")
        return
    try:
        summary = wikipedia.summary(query, sentences=3)
        kaori.send_message(msg.chat.id, f"🌻 {summary}")
    except:
        kaori.send_message(msg.chat.id, "❌ Não encontrei")

# -------------------------
# MEME
# -------------------------
@kaori.message_handler(commands=['meme'])
def meme(msg):
    try:
        r = requests.get("https://meme-api.com/gimme/ptmemes").json()
        kaori.send_photo(msg.chat.id, r['url'], caption=r['title'])
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar meme.")

# -------------------------
# GIF ALEATÓRIO
# -------------------------
@kaori.message_handler(commands=['gif'])
def gif(msg):
    query = msg.text.replace("/gif", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/gif termo")
        return
    try:
        r = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={query}&limit=10").json()
        if r.get("data"):
            url = random.choice(r["data"])["images"]["original"]["url"]
            kaori.send_animation(msg.chat.id, url)
        else:
            kaori.send_message(msg.chat.id, "❌ Nenhum gif encontrado.")
    except:
        kaori.send_message(msg.chat.id, "❌ Erro ao buscar gif.")

# -------------------------
# FIGURINHA e FIG GIF
# -------------------------
@kaori.message_handler(content_types=['photo'])
def sticker(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/img.png", "wb") as f:
            f.write(downloaded)

        img = Image.open("temp/img.png").convert("RGBA")
        img.thumbnail((512,512))
        img.save("temp/sticker.webp", "WEBP")
        with open("temp/sticker.webp", "rb") as s:
            kaori.send_sticker(msg.chat.id, s)
    except Exception as e:
        kaori.send_message(msg.chat.id, f"Erro:\n{e}")

@kaori.message_handler(commands=['envgif'])
def envgif(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        if msg.reply_to_message and msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        else:
            kaori.reply_to(msg, "Responda a imagem que quer transformar em GIF.")
            return
        file_info = kaori.get_file(file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/img.png", "wb") as f:
            f.write(downloaded)
        img = Image.open("temp/img.png")
        img.thumbnail((512,512))
        img.save("temp/sticker.gif", save_all=True, append_images=[img], loop=0, duration=200)
        with open("temp/sticker.gif", "rb") as s:
            kaori.send_document(msg.chat.id, s)
    except Exception as e:
        kaori.send_message(msg.chat.id, f"Erro:\n{e}")

# -------------------------
# /PLAY corrigido
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play", "").strip()
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
            "default_search": "ytsearch",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "extractor_args": {"youtube": {"player_client": ["android"]}},
            "http_headers": {"User-Agent": "com.google.android.youtube/17.31.35 (Linux; U; Android 11)"},
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
        with open(filename, "rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=title)
        kaori.edit_message_text(f"🎵 Tocando: {title}", msg.chat.id, status.message_id)
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# RUN
# -------------------------
print("🌻 Kaori iniciada")
kaori.infinity_polling()