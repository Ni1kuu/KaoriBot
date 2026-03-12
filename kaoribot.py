import os
import time
import telebot
import requests
from PIL import Image
from spotdl import Spotdl

# -------------------------
# CONFIGURAÇÕES
# -------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

kaori = telebot.TeleBot(BOT_TOKEN)

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

Eu sou **Kaori**, sua assistente para deixar o grupo mais divertido.

🌻 Posso:

🎧 baixar músicas
🖼 buscar imagens
🔎 pesquisar na web
✨ criar figurinhas

Use:

/menu

para ver todos os comandos disponíveis
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# MENU
# -------------------------
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
/play música ou link Spotify/SoundCloud

🖼 Figurinhas
envie uma imagem

🌟 Diversão
/joke → piada
/fact → curiosidade
/quote → frase aleatória

╰━━━━━━━━━━━━━━━━━━━━╯
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
╭━━━🌻 KAORI INFO 🌻━━━╮

🌻 Versão: {BOT_VERSION}
👤 Criador: {CREATOR}
⚡ Ping: {ping}s
⏱ Uptime: {h}h {m}m {s}s

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# PING
# -------------------------
@kaori.message_handler(commands=['ping'])
def ping(msg):
    start = time.time()
    status = kaori.send_message(msg.chat.id, "🏓 Ping...")
    end = round((time.time() - start) * 1000)
    kaori.edit_message_text(f"🏓 Pong! {end}ms", msg.chat.id, status.message_id)

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
    kaori.send_message(msg.chat.id, f"🔎 Resultado para:\n{query}\n\n{link}")

# -------------------------
# WIKI SEARCH
# -------------------------
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    import wikipedia
    query = msg.text.replace("/wiki", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/wiki termo")
        return
    try:
        resumo = wikipedia.summary(query, sentences=3, auto_suggest=False, redirect=True)
        kaori.send_message(msg.chat.id, f"🌐 {query}:\n{resumo}")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"❌ Erro: {e}")

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
        os.makedirs("temp", exist_ok=True)
        path = f"temp/img.png"
        with open(path, "wb") as f:
            f.write(downloaded)
        img = Image.open(path).convert("RGBA")
        img.thumbnail((512,512), Image.Resampling.LANCZOS)
        sticker_path = "temp/sticker.webp"
        img.save(sticker_path, "WEBP")
        with open(sticker_path, "rb") as s:
            kaori.send_sticker(msg.chat.id, s)
        os.remove(path)
        os.remove(sticker_path)
    except Exception as e:
        kaori.send_message(msg.chat.id, f"⚠️ Erro:\n{e}")

# -------------------------
# PLAY MUSIC (Spotify + SoundCloud)
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play", "").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/play nome ou link da música")
        return

    status = kaori.send_message(msg.chat.id, f"🎧 Procurando: {query}")

    try:
        os.makedirs("music", exist_ok=True)
        s = Spotdl(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        file_path = s.download_track(query)  # retorna o caminho do mp3 baixado
        kaori.edit_message_text(f"🎵 Enviando: {os.path.basename(file_path)}", msg.chat.id, status.message_id)
        with open(file_path, "rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=os.path.basename(file_path))
        os.remove(file_path)
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# PIN / UNPIN
# -------------------------
@kaori.message_handler(commands=['pin'])
def pin(msg):
    if msg.reply_to_message:
        kaori.pin_chat_message(msg.chat.id, msg.reply_to_message.message_id)

@kaori.message_handler(commands=['unpin'])
def unpin(msg):
    kaori.unpin_all_chat_messages(msg.chat.id)

# -------------------------
# JOKE / FACT / QUOTE
# -------------------------
@kaori.message_handler(commands=['joke'])
def joke(msg):
    r = requests.get("https://v2.jokeapi.dev/joke/Any?lang=pt").json()
    if r.get("type") == "single":
        kaori.send_message(msg.chat.id, r.get("joke"))
    else:
        kaori.send_message(msg.chat.id, f"{r.get('setup')}\n\n{r.get('delivery')}")

@kaori.message_handler(commands=['fact'])
def fact(msg):
    r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()
    kaori.send_message(msg.chat.id, r.get("text"))

@kaori.message_handler(commands=['quote'])
def quote(msg):
    r = requests.get("https://api.quotable.io/random?tags=technology,famous-quotes").json()
    kaori.send_message(msg.chat.id, f"💡 {r.get('content')} — {r.get('author')}")

# -------------------------
# RUN
# -------------------------
print("🌻 Kaori iniciada com sucesso!")
kaori.infinity_polling()