import os
import time
import telebot
import requests
import yt_dlp
from PIL import Image
import wikipedia
from io import BytesIO

# -------------------------
# VARIÁVEIS
# -------------------------

TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")

BOT_VERSION = "2.3"
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

    texto = """
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

👤 Usuário
/start → iniciar
/menu → comandos
/info → informações

⚡ Sistema
/ping → ping

🔎 Pesquisa
/google texto
/img imagem
/wiki termo

🎧 Música
/play nome ou link

🖼 Figurinhas
envie imagem

😂 Diversão
/joke
/fact

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
        kaori.reply_to(msg, "Use:\n/img imagem")
        return

    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"

    r = requests.get(url).json()

    if r["hits"]:
        kaori.send_photo(msg.chat.id, r["hits"][0]["largeImageURL"])
    else:
        kaori.send_message(msg.chat.id, "❌ Nenhuma imagem")

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

    except Exception:

        kaori.send_message(msg.chat.id, "❌ Não encontrei")

# -------------------------
# JOKE
# -------------------------

@kaori.message_handler(commands=['joke'])
def joke(msg):

    try:

        r = requests.get("https://v2.jokeapi.dev/joke/Any?lang=pt").json()

        if r["type"] == "single":
            kaori.send_message(msg.chat.id, r["joke"])
        else:
            kaori.send_message(msg.chat.id, f"{r['setup']}\n{r['delivery']}")

    except:

        kaori.send_message(msg.chat.id, "Erro ao buscar piada")

# -------------------------
# FACT
# -------------------------

@kaori.message_handler(commands=['fact'])
def fact(msg):

    try:

        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()

        kaori.send_message(msg.chat.id, r["text"])

    except:

        kaori.send_message(msg.chat.id, "Erro ao buscar fato")

# -------------------------
# STICKER
# -------------------------

@kaori.message_handler(content_types=['photo'])
def sticker(msg):

    try:

        os.makedirs("temp", exist_ok=True)

        file_info = kaori.get_file(msg.photo[-1].file_id)

        downloaded = kaori.download_file(file_info.file_path)

        with open("temp/img.png","wb") as f:
            f.write(downloaded)

        img = Image.open("temp/img.png").convert("RGBA")

        img.thumbnail((512,512))

        img.save("temp/sticker.webp","WEBP")

        with open("temp/sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id,s)

    except Exception as e:

        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# -------------------------
# /PLAY
# -------------------------

@kaori.message_handler(commands=['play'])
def play(msg):

    query = msg.text.replace("/play","").strip()

    chat_id = msg.chat.id

    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/play nome ou link")
        return

    status = kaori.send_message(chat_id,f"🎧 Procurando: {query}")

    try:

        os.makedirs("music",exist_ok=True)

        ydl_opts = {
            "format":"bestaudio",
            "outtmpl":"music/audio.%(ext)s",
            "noplaylist":True,
            "quiet":True,
            "default_search":"ytsearch",
            "nocheckcertificate":True
        }

       filename = ydl.prepare_filename(info)

if not os.path.exists(filename):
    for ext in ["webm","m4a","mp3","opus"]:
        test = f"music/audio.{ext}"
        if os.path.exists(test):
            filename = test
            break

        if thumb:

            t = requests.get(thumb)

            kaori.send_photo(chat_id,BytesIO(t.content),
            caption=f"🎵 {title}\n\n{progress_bar(duration)}")

        with open(filename,"rb") as audio:

            kaori.send_audio(chat_id,audio,title=title)

        kaori.edit_message_text(f"🎧 Tocando: {title}",chat_id,status.message_id)

    except Exception as e:

        kaori.edit_message_text(f"⚠️ Erro:\n{e}",chat_id,status.message_id)

# -------------------------
# RUN
# -------------------------

print("🌻 Kaori iniciada")

kaori.infinity_polling()