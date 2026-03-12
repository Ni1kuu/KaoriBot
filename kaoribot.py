import telebot
import requests
import time
import os
import random
from PIL import Image
from io import BytesIO

# 🔑 Configurações
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram token do Railway
PIXABAY_KEY = os.getenv("PIXABAY_KEY")  # Pixabay API Key
BOT_VERSION = "2.2"
CREATOR = "@ni1ckkj"

kaori = telebot.TeleBot(BOT_TOKEN)
start_time = time.time()

# -------------------------
# COMANDOS /START e /MENU
# -------------------------
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = f"""
╭━━━🌻 COMANDOS KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ✨
Eu sou Kaori, sua assistente de grupo.

🌻 Posso:

🎧 Baixar músicas
🖼 Buscar imagens
🔎 Pesquisar na web
✨ Criar figurinhas

Use:
/menu

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

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

🎧 Música
/play nome ou link → baixar música do SoundCloud/Spotify

🖼 Figurinhas
envie uma imagem → virar figurinha

😂 Diversão
/joke → piada
/fact → curiosidade
/quote → citação motivacional

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
    ping = round((time.time() - msg.date), 3)

    texto = f"""
╭━━━🌻 INFORMAÇÕES KAORI 🌻━━━╮

🌻 Versão: {BOT_VERSION}
👤 Criador: {CREATOR}
⚡ Ping: {ping}s
⏱ Uptime: {h}h {m}m {s}s

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# -------------------------
# COMANDO /PING
# -------------------------
@kaori.message_handler(commands=['ping'])
def ping(msg):
    ms = round((time.time() - msg.date) * 1000)
    kaori.reply_to(msg, f"🌻 Pong! {ms}ms")

# -------------------------
# COMANDO /GOOGLE
# -------------------------
@kaori.message_handler(commands=['google'])
def google(msg):
    query = msg.text.replace("/google","").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/google pesquisa")
        return
    link = f"https://www.google.com/search?q={query}"
    kaori.send_message(msg.chat.id, f"🔎 Resultado para:\n{query}\n\n{link}")

# -------------------------
# COMANDO /IMG
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
# FIGURINHAS AUTOMÁTICAS
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
            kaori.send_sticker(msg.chat.id,s)
        os.remove("img.png")
        os.remove("sticker.webp")
    except Exception as e:
        kaori.send_message(msg.chat.id,f"⚠️ Erro:\n{e}")

# -------------------------
# COMANDOS DE DIVERSÃO
# -------------------------
@kaori.message_handler(commands=['joke'])
def joke(msg):
    piadas = [
        "Por que o livro foi ao médico? Porque ele tinha muitas páginas!",
        "O que é verde e fica no canto da sala? Um canto verde 😆",
        "Por que o computador foi ao médico? Porque estava com vírus!"
    ]
    kaori.send_message(msg.chat.id, random.choice(piadas))

@kaori.message_handler(commands=['fact'])
def fact(msg):
    curiosidades = [
        "O mel nunca estraga.",
        "As girafas não têm cordas vocais.",
        "Os crocodilos não conseguem colocar a língua para fora."
    ]
    kaori.send_message(msg.chat.id, random.choice(curiosidades))

@kaori.message_handler(commands=['quote'])
def quote(msg):
    citacoes = [
        "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
        "Acredite em si mesmo!",
        "Faça hoje o que outros não querem, amanhã terá o que outros sonham."
    ]
    kaori.send_message(msg.chat.id, random.choice(citacoes))

# -------------------------
# COMANDO /PLAY - SoundCloud / Spotify
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        kaori.reply_to(msg,"🌻 Use:\n/play nome ou link da música")
        return

    status = kaori.send_message(msg.chat.id,f"🎧 Procurando: {query}")

    try:
        from spotdl import Spotdl
        s = Spotdl()
        # baixa música para arquivo temporário
        filename = s.download(query, output="music.mp3")
        kaori.edit_message_text(f"🎵 Enviando música...", msg.chat.id, status.message_id)
        with open("music.mp3","rb") as audio:
            kaori.send_audio(msg.chat.id,audio)
        os.remove("music.mp3")
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# EXECUTAR BOT
# -------------------------
print("🌻 Kaori iniciada")
kaori.infinity_polling()