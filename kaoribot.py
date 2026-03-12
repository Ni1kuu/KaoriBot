import telebot
import requests
import time
import os
import yt_dlp
from PIL import Image

# ==============================
# CONFIG
# ==============================

BOT_VERSION = "1.9"
CREATOR = "@ni1ckkj"

BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")

kaori = telebot.TeleBot(BOT_TOKEN)

start_time = time.time()

# ==============================
# START
# ==============================

@kaori.message_handler(commands=['start'])
def start(msg):

    texto = f"""
╭━━━🌻 KAORI BOT 🌻━━━╮

Olá {msg.from_user.first_name} ✨

Eu sou a **Kaori**, uma assistente para
deixar seu grupo mais divertido!

Use:

/menu

para ver todos os comandos 🌻

Versão: {BOT_VERSION}

╰━━━━━━━━━━━━━━━━━━╯
"""

    kaori.send_message(msg.chat.id, texto)

# ==============================
# MENU
# ==============================

@kaori.message_handler(commands=['menu'])
def menu(msg):

    texto = """
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

👤 Usuário
/start → iniciar bot
/menu → abrir comandos
/info → informações

⚡ Sistema
/ping → ping em ms

🔎 Pesquisa
/google texto
/img imagem

🎧 Música
/play música

🖼 Figurinhas
envie uma imagem

╰━━━━━━━━━━━━━━━━━━━━╯
"""

    kaori.send_message(msg.chat.id, texto)

# ==============================
# INFO
# ==============================

@kaori.message_handler(commands=['info'])
def info(msg):

    uptime = int(time.time() - start_time)

    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60

    texto = f"""
╭━━━🌻 KAORI INFO 🌻━━━╮

Versão: {BOT_VERSION}

Criador:
{CREATOR}

Uptime:
{h}h {m}m {s}s

╰━━━━━━━━━━━━━━━━━━╯
"""

    kaori.send_message(msg.chat.id, texto)

# ==============================
# PING
# ==============================

@kaori.message_handler(commands=['ping'])
def ping(msg):

    start = time.time()

    message = kaori.reply_to(msg, "🏓 Calculando ping...")

    end = time.time()

    latency = round((end - start) * 1000)

    kaori.edit_message_text(
        f"🏓 Pong!\n\n⚡ Ping: {latency} ms",
        msg.chat.id,
        message.message_id
    )

# ==============================
# GOOGLE
# ==============================

@kaori.message_handler(commands=['google'])
def google(msg):

    query = msg.text.replace("/google","").strip()

    if not query:
        kaori.reply_to(msg,"Use:\n/google pesquisa")
        return

    link = f"https://www.google.com/search?q={query}"

    kaori.send_message(
        msg.chat.id,
        f"🔎 Resultado:\n\n{link}"
    )

# ==============================
# IMAGEM PIXABAY
# ==============================

@kaori.message_handler(commands=['img'])
def img(msg):

    query = msg.text.replace("/img","").strip()

    if not query:
        kaori.reply_to(msg,"Use:\n/img nome")
        return

    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"

    r = requests.get(url).json()

    if r["hits"]:

        image = r["hits"][0]["largeImageURL"]

        kaori.send_photo(msg.chat.id,image)

    else:

        kaori.send_message(msg.chat.id,"❌ Nenhuma imagem encontrada")

# ==============================
# STICKER AUTOMÁTICO
# ==============================

@kaori.message_handler(content_types=['photo'])
def sticker(msg):

    try:

        file_info = kaori.get_file(msg.photo[-1].file_id)

        downloaded = kaori.download_file(file_info.file_path)

        with open("img.png","wb") as f:
            f.write(downloaded)

        img = Image.open("img.png").convert("RGBA")

        img.thumbnail((512,512))

        img.save("sticker.webp","WEBP")

        with open("sticker.webp","rb") as s:

            kaori.send_sticker(msg.chat.id,s)

        os.remove("img.png")
        os.remove("sticker.webp")

    except Exception as e:

        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# ==============================
# PLAY MUSIC
# ==============================

@kaori.message_handler(commands=['play'])
def play(msg):

    query = msg.text.replace("/play", "").strip()

    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/play nome da música")
        return

    status = kaori.send_message(msg.chat.id, f"🎧 Procurando: {query}")

    try:

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

        filename = "music.mp3"

        with open(filename, 'rb') as audio:
            kaori.send_audio(
                msg.chat.id,
                audio,
                title=info.get("title"),
                performer=info.get("uploader")
            )

        os.remove(filename)

        kaori.edit_message_text(
            f"🎵 Música enviada\n\n{info.get('title')}",
            msg.chat.id,
            status.message_id
        )

    except Exception as e:

        kaori.edit_message_text(
            f"⚠️ Erro ao baixar música:\n{e}",
            msg.chat.id,
            status.message_id
        )

# ==============================
# START BOT
# ==============================

print("🌻 Kaori iniciou")

kaori.infinity_polling()