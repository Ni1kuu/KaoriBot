import telebot
import requests
import time
import os
import yt_dlp
from PIL import Image
import wikipedia
import random

# ===========================
# VARIÁVEIS DE AMBIENTE
# ===========================
BOT_TOKEN = os.getenv("BOT_TOKEN")       # Configurado no Railway
PIXABAY_KEY = os.getenv("PIXABAY_KEY")   # Configurado no Railway

kaori = telebot.TeleBot(BOT_TOKEN)

BOT_VERSION = "2.4"
CREATOR = "@ni1ckkj"
start_time = time.time()

# ===========================
# COMANDOS INICIAIS
# ===========================
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ✨

Eu sou Kaori, sua assistente!꒰ᐢ. .ᐢ꒱₊˚⊹ 

🌻 Posso:
🎧 baixar músicas
🖼 buscar imagens
🔎 pesquisar na web
✨ criar figurinhas

Use /menu para ver todos os comandos
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
/play música ou link

🖼 Figurinhas
envie uma imagem para criar

🤣 Diversão
/joke → piada
/fact → fato aleatório
/quote → citação

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

@kaori.message_handler(commands=['info'])
def info(msg):
    ping = round((time.time() - msg.date), 3)
    uptime = int(time.time() - start_time)
    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60
    texto = f"""
╭━━━🌻 INFORMAÇÕES KAORI 🌻━━━╮

🌻 Versão: {BOT_VERSION}
👤 Criador: {CREATOR}
⚡ Ping: {ping}s
⏱ Uptime: {h}h {m}m {s}s

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

@kaori.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    status = kaori.send_message(msg.chat.id, "🏓 Pingando...")
    elapsed = round((time.time() - start) * 1000)
    kaori.edit_message_text(f"🏓 Pong! {elapsed} ms", msg.chat.id, status.message_id)

# ===========================
# GOOGLE
# ===========================
@kaori.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/google pesquisa")
        return
    link = f"https://www.google.com/search?q={query}"
    kaori.send_message(msg.chat.id, f"🔎 Resultado para:\n{query}\n\n{link}")

# ===========================
# PIXABAY
# ===========================
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

# ===========================
# WIKI
# ===========================
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    termo = msg.text.replace("/wiki", "").strip()
    if not termo:
        kaori.reply_to(msg, "🌻 Use:\n/wiki termo")
        return
    try:
        resumo = wikipedia.summary(termo, sentences=3, auto_suggest=False)
        kaori.send_message(msg.chat.id, f"🔎 Wikipédia: {termo}\n\n{resumo}")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"❌ Não encontrei resultados para '{termo}'")

# ===========================
# JOKE / FACT / QUOTE
# ===========================
jokes = [
    "Por que o computador foi ao médico? Porque ele tinha muitos bugs!",
    "O que o gato disse para o computador? Miau, clique aqui!"
]

facts = [
    "O Sol é 330.000 vezes maior que a Terra.",
    "A água cobre 71% da superfície da Terra."
]

quotes = [
    "A vida é o que acontece enquanto você está ocupado fazendo outros planos. – John Lennon",
    "Não espere. O tempo nunca será justo. – Napoleon Hill"
]

@kaori.message_handler(commands=['joke'])
def joke(msg):
    kaori.send_message(msg.chat.id, random.choice(jokes))

@kaori.message_handler(commands=['fact'])
def fact(msg):
    kaori.send_message(msg.chat.id, random.choice(facts))

@kaori.message_handler(commands=['quote'])
def quote(msg):
    kaori.send_message(msg.chat.id, random.choice(quotes))

# ===========================
# STICKER AUTOMÁTICO
# ===========================
@kaori.message_handler(content_types=['photo'])
def sticker(msg):
    try:
        os.makedirs("temp", exist_ok=True)
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

# ===========================
# PLAY MUSIC
# ===========================
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/play música ou link")
        return
    status = kaori.send_message(msg.chat.id,f"🎧 Procurando: {query}")

    try:
        os.makedirs("music", exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',  # Permite buscar pelo nome
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'Música')
            thumb = info.get('thumbnail')

        if thumb:
            kaori.send_photo(msg.chat.id, thumb, caption=f"🎵 {title}")

        with open(filename, "rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=title)

        os.remove(filename)
        kaori.edit_message_text(f"✅ Música enviada: {title}", msg.chat.id, status.message_id)

    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# ===========================
# RUN
# ===========================
print("🌻 Kaori iniciada")
kaori.infinity_polling()