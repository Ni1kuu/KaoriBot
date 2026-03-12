import telebot
import requests
import time
import os
import yt_dlp
from PIL import Image
from datetime import datetime

# Pegando as variáveis do Railway
TOKEN = os.environ.get("BOT_TOKEN")
PIXABAY_KEY = os.environ.get("PIXABAY_KEY")

kaori = telebot.TeleBot(TOKEN)

BOT_VERSION = "2.2"
CREATOR = "@ni1ckkj"

start_time = time.time()

# -------------------------
# START
# -------------------------
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ✨

Eu sou a Kaori, sua assistente para tornar seu grupo mais divertido e útil ꒰ᐢ. .ᐢ꒱₊˚⊹.

🌻 Posso:
🎧 baixar músicas
🖼 buscar imagens
🔎 pesquisar na web
✨ criar figurinhas

Use:
/menu
para ver todos os comandos disponíveis 🌻
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# MENU
# -------------------------
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
/google texto → pesquisar
/img imagem → buscar imagem
/wiki termo → resumo Wikipédia

🎧 Música
/play link ou nome → baixar música do YouTube ou SoundCloud

🖼 Figurinhas
envie uma imagem → virar figurinha

🤖 Diversão
/joke → piadas
/fact → curiosidades
/quote → frase aleatória

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# INFO
# -------------------------
@kaori.message_handler(commands=['info'])
def info(msg):
    uptime = int(time.time() - start_time)
    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60
    texto = f"""
╭━━━🌻 INFORMAÇÕES KAORI 🌻━━━╮
🌻 Versão: {BOT_VERSION}
👤 Criador: {CREATOR}
⏱ Uptime: {h}h {m}m {s}s
📅 Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# PING
# -------------------------
@kaori.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    kaori.send_chat_action(msg.chat.id, 'typing')
    ping_ms = round((time.time() - start) * 1000)
    kaori.reply_to(msg, f"🌻 Ping: {ping_ms}ms")

# -------------------------
# GOOGLE SEARCH
# -------------------------
@kaori.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google","").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/google pesquisa")
        return
    link = f"https://www.google.com/search?q={query}"
    kaori.send_message(msg.chat.id, f"🔎 Resultado para:\n{query}\n{link}")

# -------------------------
# PIXABAY IMAGE
# -------------------------
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
        kaori.send_photo(msg.chat.id, image)
    else:
        kaori.send_message(msg.chat.id,"❌ Nenhuma imagem encontrada")

# -------------------------
# WIKIPEDIA
# -------------------------
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    query = msg.text.replace("/wiki","").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/wiki termo")
        return
    try:
        from wikipedia import summary
        res = summary(query, sentences=3, auto_suggest=False, redirect=True)
        kaori.send_message(msg.chat.id, f"🔎 Resumo de {query}:\n\n{res}")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"❌ Não encontrei nada.\n{e}")

# -------------------------
# JOKE
# -------------------------
@kaori.message_handler(commands=['joke'])
def joke(msg):
    r = requests.get("https://v2.jokeapi.dev/joke/Any?lang=pt&type=single").json()
    kaori.send_message(msg.chat.id, r.get("joke","❌ Não encontrei piada"))

# -------------------------
# FACT
# -------------------------
@kaori.message_handler(commands=['fact'])
def fact(msg):
    r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()
    kaori.send_message(msg.chat.id, r.get("text","❌ Não encontrei curiosidade"))

# -------------------------
# QUOTE
# -------------------------
@kaori.message_handler(commands=['quote'])
def quote(msg):
    r = requests.get("https://api.quotable.io/random").json()
    kaori.send_message(msg.chat.id, f"💬 {r.get('content','')} — {r.get('author','')}")

# -------------------------
# FIGURINHAS
# -------------------------
@kaori.message_handler(content_types=['photo'])
def sticker(msg):
    try:
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("img.png","wb") as f:
            f.write(downloaded)
        img = Image.open("img.png").convert("RGBA")
        img.thumbnail((512,512), Image.Resampling.LANCZOS)
        img.save("sticker.webp","WEBP")
        with open("sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id, s)
        os.remove("img.png")
        os.remove("sticker.webp")
    except Exception as e:
        kaori.send_message(msg.chat.id,f"⚠️ Erro:\n{e}")

# -------------------------
# PLAY MUSIC (YouTube + SoundCloud)
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/play link ou nome da música")
        return
    status = kaori.send_message(msg.chat.id,f"🎧 Procurando: {query}")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/app/.apt/usr/bin/ffmpeg'  # Railway buildpack
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
        kaori.edit_message_text(f"🎵 Enviando: {info['title']}", msg.chat.id, status.message_id)
        audio_file = filename.rsplit('.',1)[0]+'.mp3'
        with open(audio_file,"rb") as audio:
            kaori.send_audio(msg.chat.id,audio,title=info['title'])
        os.remove(audio_file)
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# PIN / UNPIN
# -------------------------
@kaori.message_handler(commands=['pin'])
def pin(msg):
    if msg.reply_to_message:
        kaori.pin_chat_message(msg.chat.id,msg.reply_to_message.message_id)

@kaori.message_handler(commands=['unpin'])
def unpin(msg):
    kaori.unpin_all_chat_messages(msg.chat.id)

# -------------------------
# RUN BOT
# -------------------------
print("🌻 Kaori iniciada")
kaori.infinity_polling()