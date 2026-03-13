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

🎬 YouTube
/yt → baixar vídeo
/play → baixar música
/ytthumb → thumbnail
/ytinfo → informações

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
# /PLAY com yt-dlp + thumb e duração
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    import os, yt_dlp, time

    query = msg.text.replace("/play", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/play link ou nome da música")
        return

    status = kaori.send_message(msg.chat.id, f"🎧 Procurando: {query}")

    try:
        os.makedirs("music", exist_ok=True)

        # opções do yt-dlp
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "music/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "extractor_args": {
                "youtube": {"player_client": ["android"]}
            },
            "http_headers": {
                "User-Agent": "com.google.android.youtube/17.31.35 (Linux; U; Android 11)"
            },
            "default_search": "ytsearch",  # busca no YouTube se não for link
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

        # baixa a música
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)

        # corrige audio.NA caso necessário
        if not os.path.exists(filename):
            for ext in ["mp3","webm","m4a","opus"]:
                test = f"music/{info['title']}.{ext}"
                if os.path.exists(test):
                    filename = test
                    break

        title = info.get("title")
        thumb = info.get("thumbnail")
        duration = info.get("duration")  # em segundos

        # calcula minutos e segundos de forma segura
        if duration:
            minutos = duration // 60
            segundos = duration % 60
            tempo = f"{minutos}:{segundos:02d}"
        else:
            tempo = "desconhecido"

        # envia thumb como foto
        if thumb:
            kaori.send_photo(msg.chat.id, thumb, caption=f"🎵 {title}\n⏱ {tempo}")

        # envia áudio
        with open(filename, "rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=title)

        # atualiza mensagem de status
        kaori.edit_message_text(f"🎵 Tocando: {title}", msg.chat.id, status.message_id)

    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# /YTTHUMB pegar thumbnail
# -------------------------
@kaori.message_handler(commands=['ytthumb'])
def ytthumb(msg):
    import yt_dlp

    query = msg.text.replace("/ytthumb", "").strip()

    if not query:
        kaori.reply_to(msg, "📸 Use:\n/ytthumb link ou nome")
        return

    try:
        ydl_opts = {
            "quiet": True,
            "default_search": "ytsearch1"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

        thumb = info.get("thumbnail")
        title = info.get("title")

        kaori.send_photo(msg.chat.id, thumb, caption=f"📸 {title}")

    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar thumbnail.")

# -------------------------
# /YTINFO informações do vídeo
# -------------------------
@kaori.message_handler(commands=['ytinfo'])
def ytinfo(msg):
    import yt_dlp

    query = msg.text.replace("/ytinfo", "").strip()

    if not query:
        kaori.reply_to(msg, "📺 Use:\n/ytinfo link ou nome")
        return

    try:
        ydl_opts = {
            "quiet": True,
            "default_search": "ytsearch1"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

        title = info.get("title")
        channel = info.get("uploader")
        views = info.get("view_count")
        duration = info.get("duration")

        if duration:
            minutos = duration // 60
            segundos = duration % 60
            tempo = f"{minutos}:{segundos:02d}"
        else:
            tempo = "?"

        texto = f"""
🎬 {title}

📺 Canal: {channel}
👁 Views: {views}
⏱ Duração: {tempo}
"""

        kaori.send_message(msg.chat.id, texto)

    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar informações.")

# -------------------------
# RUN
# -------------------------

print("🌻 Kaori iniciada")

kaori.infinity_polling()