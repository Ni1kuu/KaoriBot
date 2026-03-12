import telebot
import requests
import time
import os
from PIL import Image
from urllib.parse import quote
import yt_dlp

# -------------------------
# CONFIGURAÇÃO
# -------------------------
BOT_VERSION = "2.3.1"
CREATOR = "@ni1ckkj"

TOKEN = os.environ.get("BOT_TOKEN")
PIXABAY_KEY = os.environ.get("PIXABAY_KEY")

bot = telebot.TeleBot(TOKEN)
start_time = time.time()

# -------------------------
# /start
# -------------------------
@bot.message_handler(commands=['start'])
def start(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ✨

Eu sou **Kaori**, sua assistente para deixar seu grupo divertido e útil!

Use:

/menu

para ver todos os comandos disponíveis 🌻
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.send_message(msg.chat.id, texto)

# -------------------------
# /menu
# -------------------------
@bot.message_handler(commands=['menu'])
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
/wiki termo

🎧 Música
/play link ou nome da música

🖼 Figurinhas
envie uma imagem → virar figurinha

😂 Diversão
/joke → piada aleatória
/quote → citação aleatória
/fact → curiosidade aleatória

🛡 Administração
/pin → fixar mensagem
/unpin → desafixar

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.send_message(msg.chat.id, texto)

# -------------------------
# /info
# -------------------------
@bot.message_handler(commands=['info'])
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
    bot.send_message(msg.chat.id, texto)

# -------------------------
# /ping
# -------------------------
@bot.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    status = bot.send_message(msg.chat.id, "🌻 Pingando...")
    end = time.time()
    bot.edit_message_text(f"🌻 Pong! {round((end-start)*1000)}ms", msg.chat.id, status.message_id)

# -------------------------
# /google
# -------------------------
@bot.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google","").strip()
    if not query:
        bot.reply_to(msg,"🌻 Use:\n/google termo")
        return
    link = f"https://www.google.com/search?q={quote(query)}"
    bot.send_message(msg.chat.id,f"🔎 Resultado para:\n{query}\n\n{link}")

# -------------------------
# /img
# -------------------------
@bot.message_handler(commands=['img'])
def img(msg):
    query = msg.text.replace("/img","").strip()
    if not query:
        bot.reply_to(msg,"🌻 Use:\n/img termo")
        return
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={quote(query)}&image_type=photo"
    r = requests.get(url).json()
    if r["hits"]:
        image = r["hits"][0]["largeImageURL"]
        bot.send_photo(msg.chat.id, image)
    else:
        bot.send_message(msg.chat.id,"❌ Nenhuma imagem encontrada")

# -------------------------
# /wiki
# -------------------------
@bot.message_handler(commands=['wiki'])
def wiki(msg):
    termo = msg.text.replace("/wiki","").strip()
    if not termo:
        bot.reply_to(msg,"🌻 Use:\n/wiki termo")
        return
    termo_url = quote(termo)
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_url}"
    r = requests.get(url).json()
    if "extract" in r:
        bot.reply_to(msg,r["extract"][:800])
    else:
        bot.reply_to(msg,"❌ Não encontrei esse termo na Wikipedia.")

# -------------------------
# /play música/link
# -------------------------
@bot.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        bot.reply_to(msg,"🌻 Use:\n/play link ou nome da música")
        return
    status = bot.send_message(msg.chat.id,f"🎧 Procurando: {query}")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music/audio.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title','Música')
            thumbnail = info.get('thumbnail')
        bot.edit_message_text(f"🎵 Enviando: {title}", msg.chat.id, status.message_id)
        # envia thumbnail se houver
        if thumbnail:
            bot.send_photo(msg.chat.id, thumbnail, caption=f"🎵 {title}")
        with open(filename,"rb") as audio:
            bot.send_audio(msg.chat.id, audio, title=title)
    except Exception as e:
        bot.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# Figurinhas automáticas
# -------------------------
@bot.message_handler(content_types=['photo'])
def sticker(msg):
    try:
        file_info = bot.get_file(msg.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("img.png","wb") as f:
            f.write(downloaded)
        img = Image.open("img.png").convert("RGBA")
        img.thumbnail((512,512), Image.Resampling.LANCZOS)
        img.save("sticker.webp","WEBP")
        with open("sticker.webp","rb") as s:
            bot.send_sticker(msg.chat.id,s)
        os.remove("img.png")
        os.remove("sticker.webp")
    except Exception as e:
        bot.send_message(msg.chat.id,f"⚠️ Erro:\n{e}")

# -------------------------
# /pin
# -------------------------
@bot.message_handler(commands=['pin'])
def pin(msg):
    if msg.reply_to_message:
        bot.pin_chat_message(msg.chat.id, msg.reply_to_message.message_id)

# -------------------------
# /unpin
# -------------------------
@bot.message_handler(commands=['unpin'])
def unpin(msg):
    bot.unpin_all_chat_messages(msg.chat.id)

# -------------------------
# Comandos de diversão
# -------------------------
@bot.message_handler(commands=['joke'])
def joke(msg):
    r = requests.get("https://v2.jokeapi.dev/joke/Any").json()
    if r.get("type")=="single":
        bot.reply_to(msg,r.get("joke"))
    else:
        bot.reply_to(msg,f"{r.get('setup')}\n{r.get('delivery')}")

@bot.message_handler(commands=['quote'])
def quote(msg):
    r = requests.get("https://api.quotable.io/random").json()
    bot.reply_to(msg,f"{r.get('content')} — {r.get('author')}")

@bot.message_handler(commands=['fact'])
def fact(msg):
    r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()
    bot.reply_to(msg,r.get("text"))

# -------------------------
# RUN
# -------------------------
print("🌻 Kaori iniciada")
bot.infinity_polling()