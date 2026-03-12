import os
import time
import shlex
import subprocess
import telebot
import requests
from PIL import Image
import wikipedia

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
BOT_VERSION = "2.2"
CREATOR = "@ni1ckkj"
start_time = time.time()

kaori = telebot.TeleBot(TOKEN)

# -------------------------
# /START e /MENU
# -------------------------
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ✨
Eu sou **Kaori**, sua assistente do Telegram.

Use /menu para ver todos os comandos disponíveis 🌻
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

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
/wiki termo

🎧 Música
/play nome ou link

🖼 Figurinhas
envie uma imagem

😂 Diversão
/joke → piada
/fact → curiosidade

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
# GOOGLE SEARCH
# -------------------------
@kaori.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/google termo")
        return
    link = f"https://www.google.com/search?q={query}"
    kaori.send_message(msg.chat.id, f"🔎 Resultado para: {query}\n{link}")

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
# WIKIPEDIA
# -------------------------
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    query = msg.text.replace("/wiki", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/wiki termo")
        return
    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
        kaori.send_message(msg.chat.id, f"🌻 Wikipedia:\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        kaori.send_message(msg.chat.id, f"⚠️ Termo ambíguo. Sugestões: {e.options[:5]}")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"❌ Erro ao buscar: {e}")

# -------------------------
# /JOKE e /FACT
# -------------------------
@kaori.message_handler(commands=['joke'])
def joke(msg):
    try:
        r = requests.get("https://v2.jokeapi.dev/joke/Programming?lang=pt").json()
        if r['type'] == 'single':
            kaori.send_message(msg.chat.id, f"😂 {r['joke']}")
        else:
            kaori.send_message(msg.chat.id, f"😂 {r['setup']}\n💡 {r['delivery']}")
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui buscar uma piada agora.")

@kaori.message_handler(commands=['fact'])
def fact(msg):
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()
        kaori.send_message(msg.chat.id, f"🌟 {r['text']}")
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui buscar um fato agora.")

# -------------------------
# FIGURINHAS
# -------------------------
@kaori.message_handler(content_types=['photo'])
def sticker(msg):
    try:
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/img.png", "wb") as f:
            f.write(downloaded)
        img = Image.open("temp/img.png").convert("RGBA")
        img.thumbnail((512,512), Image.Resampling.LANCZOS)
        img.save("temp/sticker.webp", "WEBP")
        with open("temp/sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id, s)
        os.remove("temp/img.png")
        os.remove("temp/sticker.webp")
    except Exception as e:
        kaori.send_message(msg.chat.id,f"⚠️ Erro:\n{e}")

# -------------------------
# /PLAY com SpotDL CLI
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    import os, re, shlex, subprocess

    query = msg.text.replace("/play", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/play link ou nome da música")
        return

    status = kaori.send_message(msg.chat.id, f"🎧 Procurando: {query}")

    try:
        # garante que a pasta music exista
        os.makedirs("music", exist_ok=True)

        # Detecta se é link ou nome
        if re.match(r'https?://', query):
            # Link direto
            cmd = f"spotdl {shlex.quote(query)} --output music/audio.mp3 --overwrite"
        else:
            # Nome da música → busca no YouTube
            cmd = f"spotdl {shlex.quote(query)} --output music/audio.mp3 --overwrite --default-search ytsearch"

        # Executa o SpotDL
        subprocess.run(cmd, shell=True, check=True)

        # Envia o áudio
        with open("music/audio.mp3", "rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=query)

        kaori.edit_message_text(f"🎵 {query}", msg.chat.id, status.message_id)

    except subprocess.CalledProcessError as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# RUN BOT
# -------------------------
print("🌻 Kaori iniciada")
kaori.infinity_polling()