import telebot
import requests
import time
import os
import yt_dlp
from PIL import Image

TOKEN = "SEU_TOKEN_AQUI"
PIXABAY_KEY = "SUA_PIXABAY_KEY"

kaori = telebot.TeleBot(TOKEN)

BOT_VERSION = "1.8.3"
CREATOR = "@ni1ckkj"

start_time = time.time()

# -------------------------
# START
# -------------------------

@kaori.message_handler(commands=['start'])
def start(msg):

    texto = f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        🌻 Bem‑vindo à Kaori 🌻
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

Olá {msg.from_user.first_name} ✨

Eu sou **Kaori**, uma assistente criada para
tornar seu grupo mais divertido e útil.

🌻 Posso:

🎧 baixar músicas
🖼 buscar imagens
🔎 pesquisar na web
✨ criar figurinhas

Use:

/menu

para ver todos os comandos disponíveis 🌻
"""

    kaori.send_message(msg.chat.id, texto)

# -------------------------
# MENU
# -------------------------

@kaori.message_handler(commands=['menu'])
def menu(msg):

    texto = """
╭━━━━━━━━━━━━━━━🌻 KAORI 🌻━━━━━━━━━━━━━━━╮

👤 Usuário
├ /start → iniciar
├ /menu → abrir menu
├ /info → informações do bot

🔎 Pesquisa
├ /google texto → pesquisar
├ /img nome → buscar imagem

🎧 Música
├ /play música → baixar música

🖼 Figurinhas
├ envie uma imagem → virar figurinha

🛡 Administração
├ /pin → fixar mensagem
├ /unpin → desafixar

╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""

    kaori.send_message(msg.chat.id, texto)

# -------------------------
# INFO
# -------------------------

@kaori.message_handler(commands=['info'])
def info(msg):

    ping = round((time.time() - msg.date), 3)

    uptime = int(time.time() - start_time)

    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60

    texto = f"""
╭━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╮
        Informações da Kaori
╰━━━━━━━━━━━━━━━🌻━━━━━━━━━━━━━━━╯

🌻 Versão: {BOT_VERSION}

👤 Criador:
{CREATOR}

⚡ Ping:
{ping}s

⏱ Uptime:
{h}h {m}m {s}s
"""

    kaori.send_message(msg.chat.id, texto)

# -------------------------
# GOOGLE SEARCH
# -------------------------

@kaori.message_handler(commands=['google'])
def google(msg):

    query = msg.text.replace("/google", "").strip()

    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/google pesquisa")
        return

    link = f"https://www.google.com/search?q={query}"

    kaori.send_message(
        msg.chat.id,
        f"🔎 Resultado para:\n{query}\n\n{link}"
    )

# -------------------------
# PIXABAY IMAGE
# -------------------------

@kaori.message_handler(commands=['img'])
def img(msg):

    query = msg.text.replace("/img", "").strip()

    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/img nome da imagem")
        return

    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"

    r = requests.get(url).json()

    if r["hits"]:

        image = r["hits"][0]["largeImageURL"]

        kaori.send_photo(msg.chat.id, image)

    else:
        kaori.send_message(msg.chat.id, "❌ Nenhuma imagem encontrada")

# -------------------------
# STICKER AUTOMÁTICO
# -------------------------

@kaori.message_handler(content_types=['photo'])
def sticker(msg):

    try:

        file_info = kaori.get_file(msg.photo[-1].file_id)

        downloaded = kaori.download_file(file_info.file_path)

        with open("img.png", "wb") as f:
            f.write(downloaded)

        img = Image.open("img.png").convert("RGBA")

        img.thumbnail((512,512), Image.Resampling.LANCZOS)

        img.save("sticker.webp", "WEBP")

        with open("sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id, s)

        os.remove("img.png")
        os.remove("sticker.webp")

    except Exception as e:
        kaori.send_message(msg.chat.id,f"⚠️ Erro:\n{e}")

# -------------------------
# PLAY MUSIC
# -------------------------

@kaori.message_handler(commands=['play'])
def play(msg):

    query = msg.text.replace("/play","").strip()

    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/play nome da música")
        return

    status = kaori.send_message(msg.chat.id,f"🎧 Procurando: {query}")

    try:

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(query, download=True)

            title = info['title']

        kaori.edit_message_text(
            f"🎵 Enviando:\n{title}",
            msg.chat.id,
            status.message_id
        )

        with open("music.mp3","rb") as audio:
            kaori.send_audio(msg.chat.id,audio,title=title)

        os.remove("music.mp3")

    except Exception as e:

        kaori.edit_message_text(
            f"⚠️ Erro ao baixar música:\n{e}",
            msg.chat.id,
            status.message_id
        )

# -------------------------
# PIN
# -------------------------

@kaori.message_handler(commands=['pin'])
def pin(msg):

    if msg.reply_to_message:

        kaori.pin_chat_message(
            msg.chat.id,
            msg.reply_to_message.message_id
        )

# -------------------------
# UNPIN
# -------------------------

@kaori.message_handler(commands=['unpin'])
def unpin(msg):

    kaori.unpin_all_chat_messages(msg.chat.id)

# -------------------------
# RUN
# -------------------------

print("🌻 Kaori iniciada")

kaori.infinity_polling()