import telebot
import requests
import time
import os
import yt_dlp
from PIL import Image
from collections import deque

# ==============================
# CONFIG
# ==============================

BOT_VERSION = "3.0"

BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")

kaori = telebot.TeleBot(BOT_TOKEN)

start_time = time.time()

music_queue = deque()
downloading = False

# ==============================
# START
# ==============================

@kaori.message_handler(commands=['start'])
def start(msg):

    text = f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 Bem‑vindo à Kaori 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

Use /menu para ver comandos.

Versão: {BOT_VERSION}
"""

    kaori.send_message(msg.chat.id, text)

# ==============================
# MENU
# ==============================

@kaori.message_handler(commands=['menu'])
def menu(msg):

    text = """
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

👤 Usuário
/start
/menu
/info

⚡ Sistema
/ping

🔎 Pesquisa
/google texto
/img imagem

🎧 Música
/play música
/queue

🖼 Figurinhas
envie uma imagem

╰━━━━━━━━━━━━━━━━━━━━╯
"""

    kaori.send_message(msg.chat.id, text)

# ==============================
# INFO
# ==============================

@kaori.message_handler(commands=['info'])
def info(msg):

    uptime = int(time.time() - start_time)

    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60

    text = f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 INFO KAORI 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

Versão: {BOT_VERSION}

Uptime:
{h}h {m}m {s}s
"""

    kaori.send_message(msg.chat.id, text)

# ==============================
# PING
# ==============================

@kaori.message_handler(commands=['ping'])
def ping(msg):

    start = time.time()

    message = kaori.reply_to(msg,"🏓 Calculando...")

    end = time.time()

    latency = round((end - start)*1000)

    kaori.edit_message_text(
f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 PING KAORI 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

🏓 Pong!
⚡ {latency} ms
""",
msg.chat.id,
message.message_id)

# ==============================
# GOOGLE
# ==============================

@kaori.message_handler(commands=['google'])
def google(msg):

    query = msg.text.replace("/google","").strip()

    link = f"https://google.com/search?q={query}"

    kaori.send_message(msg.chat.id,link)

# ==============================
# IMG
# ==============================

@kaori.message_handler(commands=['img'])
def img(msg):

    query = msg.text.replace("/img","").strip()

    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"

    r = requests.get(url).json()

    if r["hits"]:
        kaori.send_photo(msg.chat.id,r["hits"][0]["largeImageURL"])

# ==============================
# STICKER
# ==============================

@kaori.message_handler(content_types=['photo'])
def sticker(msg):

    file_info = kaori.get_file(msg.photo[-1].file_id)

    downloaded = kaori.download_file(file_info.file_path)

    with open("temp/img.png","wb") as f:
        f.write(downloaded)

    img = Image.open("temp/img.png").convert("RGBA")

    img.thumbnail((512,512))

    img.save("temp/sticker.webp","WEBP")

    with open("temp/sticker.webp","rb") as s:
        kaori.send_sticker(msg.chat.id,s)

# ==============================
# MUSIC DOWNLOAD
# ==============================

def download_music(url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android','ios']
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url,download=True)

        file = ydl.prepare_filename(info)

    return file,info

# ==============================
# PLAY
# ==============================

@kaori.message_handler(commands=['play'])
def play(msg):

    global downloading

    query = msg.text.replace("/play","").strip()

    if not query:
        kaori.reply_to(msg,"Use /play música")
        return

    music_queue.append((msg.chat.id,query))

    kaori.send_message(msg.chat.id,f"🎧 Adicionado à fila:\n{query}")

    if not downloading:
        process_queue()

# ==============================
# PROCESS QUEUE
# ==============================

def process_queue():

    global downloading

    if not music_queue:
        downloading=False
        return

    downloading=True

    chat_id,query = music_queue.popleft()

    try:

        kaori.send_message(chat_id,"🎧 Baixando...")

        if "youtube.com" in query:
            url=query
        else:
            url=f"ytsearch:{query}"

        file,info=download_music(url)

        thumb=info.get("thumbnail")

        if thumb:
            kaori.send_photo(chat_id,thumb,
            caption=f"🎵 {info.get('title')}\n👤 {info.get('uploader')}")

        with open(file,"rb") as audio:
            kaori.send_audio(chat_id,audio)

        os.remove(file)

    except Exception as e:

        kaori.send_message(chat_id,f"Erro:\n{e}")

    process_queue()

# ==============================
# QUEUE
# ==============================

@kaori.message_handler(commands=['queue'])
def queue(msg):

    if not music_queue:

        kaori.send_message(msg.chat.id,"Fila vazia 🌻")

        return

    text="🎧 Fila:\n"

    for i,m in enumerate(music_queue):

        text+=f"{i+1}. {m[1]}\n"

    kaori.send_message(msg.chat.id,text)

# ==============================

print("Kaori v3.0 online")

kaori.infinity_polling()