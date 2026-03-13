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
GENIUS_KEY = os.getenv("GENIUS_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OWM_KEY = os.getenv("OWM_KEY")
GIPHY_KEY = os.getenv("GIPHY_KEY")

BOT_VERSION = "2.6.2"
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
/google termo
/gif termo
/meme → meme em português
/quote → quote aleatória

🎬 YouTube
/play → baixar música
/ytthumb → thumbnail
/ytinfo → informações

🎶 Música
/lyrics → letra da música

🎨 Diversão e arte
/anime → imagem de anime aleatória
/envgif → vídeo para gif
/fig → responder imagem ou GIF para sticker
/merece → frase motivacional

🌤 Clima
/clima cidade → clima da cidade

🧠 IA
/ai → resposta estilo IA

🎲 Diversão rápida
/8ball → bola 8
/dice → jogar dado
/calc → calculadora

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
# /FIG - responder imagem ou GIF
# -------------------------
@kaori.message_handler(commands=['fig'])
def fig(msg):
    try:
        if not msg.reply_to_message:
            kaori.send_message(msg.chat.id, "⚠️ Responda a uma imagem ou GIF com /fig")
            return

        replied = msg.reply_to_message
        os.makedirs("temp", exist_ok=True)

        # Definir arquivo e extensão
        if replied.content_type == "photo":
            file_info = kaori.get_file(replied.photo[-1].file_id)
            ext = "png"
        elif replied.content_type == "animation":
            file_info = kaori.get_file(replied.animation.file_id)
            ext = "gif"
        else:
            kaori.send_message(msg.chat.id, "❌ Apenas imagens ou GIFs podem virar figurinha")
            return

        input_path = f"temp/input.{ext}"
        downloaded = kaori.download_file(file_info.file_path)
        with open(input_path, "wb") as f:
            f.write(downloaded)

        if ext == "png":
            # Imagem estática
            img = Image.open(input_path).convert("RGBA")
            img.thumbnail((512, 512))
            img.save("temp/sticker.webp", "WEBP")
            with open("temp/sticker.webp", "rb") as s:
                kaori.send_sticker(msg.chat.id, s)
        else:
            # GIF animado → WEBP animado
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(input_path)
            clip = clip.resize(height=512)  # tamanho máximo 512px
            clip.write_gif("temp/temp.gif")  # cria GIF temporário
            clip.write_videofile("temp/temp.mp4", fps=30, codec="libvpx")  # opcional para checar frames
            # Agora convertemos para webp animado usando Pillow + imageio
            import imageio
            frames = imageio.mimread("temp/temp.gif")
            imageio.mimsave("temp/sticker.webp", frames, format='WEBP', duration=clip.duration/len(frames))
            with open("temp/sticker.webp", "rb") as s:
                kaori.send_sticker(msg.chat.id, s)

    except Exception as e:
        kaori.send_message(msg.chat.id, f"❌ Erro ao criar figurinha:\n{e}")

# -------------------------
# RUN
# -------------------------
print(f"🌻 Kaori {BOT_VERSION} iniciada")
kaori.infinity_polling()