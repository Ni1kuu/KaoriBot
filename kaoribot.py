import os
import time
import telebot
import requests
import yt_dlp
from PIL import Image
import wikipedia
from io import BytesIO
import random
import math

# -------------------------
# VARIÁVEIS
# -------------------------

TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")
GENIUS_KEY = os.getenv("GENIUS_KEY")
OWM_KEY = os.getenv("OWM_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

BOT_VERSION = "2.6.1"
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
    texto = f"""
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
/gif termo

🎬 YouTube
/yt → baixar vídeo
/play → baixar música
/ytthumb → thumbnail
/ytinfo → informações

🎶 Música
/lyrics → letra da música

🎨 Diversão e arte
/anime → imagem de anime aleatória
/meme → meme aleatório
/envgif → vídeo para gif
/quote → quote aleatória
/merece → frase motivacional

🌤 Clima
/clima cidade → clima da cidade

🧠 IA
/ai → resposta estilo IA

🎲 Diversão rápida
/8ball → bola 8
/dice → jogar dado
/calc → calculadora

🖼 Figurinhas
envie imagem ou vídeo

😂 Diversão
/joke → piada
/jokeimg → piada em imagem
/fact → fato aleatório

╰━━━━━━━━━━━━━━━━━━━━╯
Versão: {BOT_VERSION}
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
# /GOOGLE
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
# /IMG
# -------------------------
@kaori.message_handler(commands=['img'])
def img(msg):
    if not PIXABAY_KEY:
        kaori.send_message(msg.chat.id, "❌ API key do Pixabay não configurada")
        return
    query = msg.text.replace("/img", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/img termo")
        return
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"
    r = requests.get(url).json()
    if r.get("hits"):
        kaori.send_photo(msg.chat.id, r["hits"][0]["largeImageURL"])
    else:
        kaori.send_message(msg.chat.id, "❌ Nenhuma imagem encontrada")

# -------------------------
# /GIF
# -------------------------
@kaori.message_handler(commands=['gif'])
def gif(msg):
    if not GIPHY_KEY:
        kaori.send_message(msg.chat.id, "❌ API key do Giphy não configurada")
        return
    query = msg.text.replace("/gif", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/gif termo")
        return
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={query}&limit=1&rating=g"
    r = requests.get(url).json()
    try:
        gif_url = r["data"][0]["images"]["original"]["url"]
        kaori.send_animation(msg.chat.id, gif_url)
    except:
        kaori.send_message(msg.chat.id, "❌ Nenhum gif encontrado")

# -------------------------
# /ANIME
# -------------------------
@kaori.message_handler(commands=['anime'])
def anime(msg):
    url = "https://api.waifu.pics/sfw/waifu"
    try:
        r = requests.get(url).json()
        kaori.send_photo(msg.chat.id, r["url"])
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar imagem de anime")

# -------------------------
# /MEME
# -------------------------
@kaori.message_handler(commands=['meme'])
def meme(msg):
    try:
        r = requests.get("https://meme-api.com/gimme/ptmemes").json()
        kaori.send_photo(msg.chat.id, r["url"], caption=r["title"])
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar meme")

# -------------------------
# /MERECE
# -------------------------
@kaori.message_handler(commands=['merece'])
def merece(msg):
    frases = [
        "Você é incrível! 🌸",
        "Continue assim, não desista! 💪",
        "Cada dia é uma nova chance ✨",
        "Você merece o melhor sempre 💖"
    ]
    kaori.send_message(msg.chat.id, random.choice(frases))

# -------------------------
# /QUOTE
# -------------------------
@kaori.message_handler(commands=['quote'])
def quote(msg):
    try:
        r = requests.get("https://api.quotable.io/random").json()
        kaori.send_message(msg.chat.id, f"💬 {r['content']} — {r['author']}")
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar quote")

# -------------------------
# /8BALL
# -------------------------
@kaori.message_handler(commands=['8ball'])
def eightball(msg):
    respostas = ["Sim", "Não", "Talvez", "Com certeza", "Não sei", "Provavelmente"]
    kaori.send_message(msg.chat.id, random.choice(respostas))

# -------------------------
# /DICE
# -------------------------
@kaori.message_handler(commands=['dice'])
def dice(msg):
    kaori.send_message(msg.chat.id, f"🎲 Resultado: {random.randint(1,6)}")

# -------------------------
# /CALC
# -------------------------
@kaori.message_handler(commands=['calc'])
def calc(msg):
    query = msg.text.replace("/calc", "").strip()
    try:
        result = eval(query)
        kaori.send_message(msg.chat.id, f"🧮 Resultado: {result}")
    except:
        kaori.send_message(msg.chat.id, "❌ Expressão inválida")

# -------------------------
# /AI
# -------------------------
@kaori.message_handler(commands=['ai'])
def ai(msg):
    if not OPENAI_KEY:
        kaori.send_message(msg.chat.id, "❌ API key do OpenAI não configurada")
        return
    query = msg.text.replace("/ai", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/ai pergunta")
        return
    try:
        import openai
        openai.api_key = OPENAI_KEY
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.7,
            max_tokens=200
        )
        kaori.send_message(msg.chat.id, response["choices"][0]["text"].strip())
    except:
        kaori.send_message(msg.chat.id, "❌ Erro ao processar IA")

# -------------------------
# /ENVGIF / STICKER
# -------------------------
@kaori.message_handler(content_types=['photo','video'])
def sticker(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        if msg.content_type == "photo":
            file_info = kaori.get_file(msg.photo[-1].file_id)
        else:
            file_info = kaori.get_file(msg.video.file_id)
        downloaded = kaori.download_file(file_info.file_path)
        ext = "png" if msg.content_type=="photo" else "mp4"
        with open(f"temp/input.{ext}","wb") as f:
            f.write(downloaded)
        if ext=="png":
            img = Image.open("temp/input.png").convert("RGBA")
            img.thumbnail((512,512))
            img.save("temp/sticker.webp","WEBP")
            with open("temp/sticker.webp","rb") as s:
                kaori.send_sticker(msg.chat.id,s)
        else:
            # converter vídeo em gif (envgif)
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip("temp/input.mp4")
            clip = clip.resize(width=512)
            clip.write_gif("temp/sticker.gif")
            with open("temp/sticker.gif","rb") as s:
                kaori.send_animation(msg.chat.id,s)
    except Exception as e:
        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# -------------------------
# RUN
# -------------------------
print(f"🌻 Kaori {BOT_VERSION} iniciada")
kaori.infinity_polling()