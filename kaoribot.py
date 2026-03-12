import os
import time
import telebot
import requests
from PIL import Image
import wikipedia
from spotdl import SpotifyDL

# -------------------------
# VARIÁVEIS
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
SPOTDL_CONFIG = {
    "client_id": os.getenv("SPOTDL_CLIENT_ID"),
    "client_secret": os.getenv("SPOTDL_CLIENT_SECRET")
}

kaori = telebot.TeleBot(TOKEN)
BOT_VERSION = "2.0.1"
CREATOR = "@ni1ckkj"
start_time = time.time()

# -------------------------
# COMANDOS /START e /MENU
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
# COMANDO /INFO
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
# COMANDO /PING
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
# JOKE e FACT
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
# STICKERS AUTOMÁTICO
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
# /PLAY COM EMBED ESTILO SPOTIFY
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play", "").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/play link ou nome da música")
        return

    status = kaori.send_message(msg.chat.id,f"🎧 Procurando: {query}")

    try:
        with SpotifyDL(SPOTDL_CONFIG) as sdl:
            info = sdl.download([query], output=f"music/{query}.mp3", return_song_objects=True)[0]
            # Embed estilo Spotify
            texto_embed = f"""
🎵 {info.name}
👤 {', '.join(info.artists)}
⏱ {int(info.duration)}s
"""
            kaori.edit_message_text(texto_embed, msg.chat.id, status.message_id)

            # Enviar áudio
            with open(f"music/{query}.mp3","rb") as audio:
                kaori.send_audio(msg.chat.id, audio, title=info.name, performer=', '.join(info.artists))

            # Enviar thumbnail
            if info.thumbnail:
                kaori.send_photo(msg.chat.id, info.thumbnail)

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
# RUN BOT
# -------------------------
print("🌻 Kaori iniciada")
kaori.infinity_polling()