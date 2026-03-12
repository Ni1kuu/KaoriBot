import telebot
import requests
import time
import os
import yt_dlp
from PIL import Image

# ==============================
# CONFIGURAÇÃO
# ==============================

BOT_VERSION = "2.1"
BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
CREATOR = "@ni1ckkj"

kaori = telebot.TeleBot(BOT_TOKEN)
start_time = time.time()

# ==============================
# START
# ==============================

@kaori.message_handler(commands=['start'])
def start(msg):

    texto = f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 Bem‑vindo à Kaori 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

Olá {msg.from_user.first_name} 🥰✨

Eu sou Kaori, sua assistente para tornar o grupo mais divertido e útil.

🌻 Posso:

🎧 Baixar músicas
🖼 Buscar imagens
🔎 Pesquisar na web
✨ Criar figurinhas

Use:

/menu

para ver todos os comandos disponíveis 🌻

Versão: {BOT_VERSION}
"""

    kaori.send_message(msg.chat.id, texto)

# ==============================
# MENU
# ==============================

@kaori.message_handler(commands=['menu'])
def menu(msg):

    texto = f"""
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
/play link → baixar música

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

    uptime_sec = int(time.time() - start_time)
    h = uptime_sec // 3600
    m = (uptime_sec % 3600) // 60
    s = uptime_sec % 60

    texto = f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 INFORMAÇÕES DA KAORI 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

🌻 Versão: {BOT_VERSION}
👤 Criador: {CREATOR}
⏱ Uptime: {h}h {m}m {s}s
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
        f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 PING KAORI 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

🏓 Pong!
⚡ Ping: {latency} ms
""",
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
        kaori.reply_to(msg,"🌻 Use:\n/google pesquisa")
        return

    link = f"https://www.google.com/search?q={query}"

    kaori.send_message(
        msg.chat.id,
        f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 RESULTADO GOOGLE 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

🔎 {query}
{link}
"""
    )

# ==============================
# IMG PIXABAY
# ==============================

@kaori.message_handler(commands=['img'])
def img(msg):

    query = msg.text.replace("/img","").strip()

    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/img nome da imagem")
        return

    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"
    r = requests.get(url).json()

    if r["hits"]:
        image = r["hits"][0]["largeImageURL"]
        kaori.send_photo(msg.chat.id,image)
    else:
        kaori.send_message(msg.chat.id,"❌ Nenhuma imagem encontrada")

# ==============================
# STICKER
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
        kaori.send_message(msg.chat.id,f"⚠️ Erro:\n{e}")

# ==============================
# PLAY MUSIC
# ==============================

@kaori.message_handler(commands=['play'])
def play(msg):

    url = msg.text.replace("/play","").strip()

    if not url:
        kaori.reply_to(msg,"🌻 Use:\n/play link_do_youtube")
        return

    status = kaori.send_message(msg.chat.id,"🎧 Baixando música...")

    try:

        ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'audio.%(ext)s',
    'quiet': True,
    'noplaylist': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android']
        }
    },
    'http_headers': {
        'User-Agent': 'com.google.android.youtube/17.31.35 (Linux; U; Android 11)'
    }
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    filename = ydl.prepare_filename(info)

        # thumbnail
        thumb = info.get("thumbnail")
        if thumb:
            kaori.send_photo(
                msg.chat.id,
                thumb,
                caption=f"🎵 {info.get('title')}\n👤 {info.get('uploader')}"
            )

        # audio
        with open(filename,'rb') as audio:
            kaori.send_audio(
                msg.chat.id,
                audio,
                title=info.get("title"),
                performer=info.get("uploader")
            )

        os.remove(filename)
        kaori.edit_message_text(
            f"🎵 Música enviada!",
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
# RUN
# ==============================

print(f"🌻 KaoriBot v{BOT_VERSION} iniciado")
kaori.infinity_polling()