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

BOT_VERSION = "2.6.3"
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
╭━━━🌻 COMANDOS DA KAORI 🌻━━━╮

Olá {msg.from_user.first_name} ꒰ᐢ. .ᐢ꒱₊˚⊹ ✨
Eu sou a Kaori, sua assistente.

Use /menu para ver comandose divirta-se!🌻

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
/ping

🔎 Pesquisa
/google texto
/img termo
/gif termo

🎬 YouTube
/play → baixar música
/ytthumb → thumbnail
/ytinfo → informações

🎶 Música
/lyrics → letra da música

🎨 Diversão e arte
/anime → imagem de anime aleatória
/meme → meme aleatório
/fig → transformar imagem em figurinha
/quote → quote aleatória
/merece → frase motivacional

🌤 Clima
/clima cidade → clima da cidade

🧠 IA
/ai → resposta estilo IA

🎲 Diversão rápida
/oracle → respostas do oráculo
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
    if r["hits"]:
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
# /ORACLE (/8BALL atualizado)
# -------------------------
respostas_oracle = [
    "Sim, sem dúvidas ✨",
    "Não conte com isso ❌",
    "Talvez, o futuro é incerto 🔮",
    "Com certeza! 💫",
    "Não sei 🤷‍♀️",
    "Provavelmente ✅",
    "Pergunte novamente mais tarde ⏳",
    "Meu conselho é… confie na sua intuição 💭",
    "As estrelas dizem que sim 🌟",
    "Não agora, espere um pouco ⏱"
]

@kaori.message_handler(commands=['oracle'])
def oracle(msg):
    kaori.send_message(msg.chat.id, random.choice(respostas_oracle))

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
# /FIG (imagem apenas)
# -------------------------
@kaori.message_handler(content_types=['photo'])
def fig(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/input.png", "wb") as f:
            f.write(downloaded)
        img = Image.open("temp/input.png").convert("RGBA")
        img.thumbnail((512,512))
        img.save("temp/sticker.webp", "WEBP")
        with open("temp/sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id,s)
    except Exception as e:
        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# -------------------------
# /PLAY
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    query = msg.text.replace("/play","").strip()
    if not query:
        kaori.reply_to(msg, "🌻 Use:\n/play link ou nome da música")
        return
    status = kaori.send_message(msg.chat.id, f"🎧 Procurando: {query}")
    try:
        os.makedirs("music", exist_ok=True)
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "music/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "default_search": "ytsearch",
            "postprocessors": [{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
        if not os.path.exists(filename):
            for ext in ["mp3","webm","m4a","opus"]:
                test = f"music/{info['title']}.{ext}"
                if os.path.exists(test):
                    filename = test
                    break
        title = info.get("title")
        with open(filename,"rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=title)
        kaori.edit_message_text(f"🎵 Tocando: {title}", msg.chat.id, status.message_id)
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# /YTTHUMB
# -------------------------
@kaori.message_handler(commands=['ytthumb'])
def ytthumb(msg):
    query = msg.text.replace("/ytthumb","").strip()
    if not query:
        kaori.reply_to(msg, "📸 Use:\n/ytthumb link ou nome")
        return
    try:
        with yt_dlp.YoutubeDL({"quiet":True,"default_search":"ytsearch1"}) as ydl:
            info = ydl.extract_info(query, download=False)
        kaori.send_photo(msg.chat.id, info.get("thumbnail"), caption=info.get("title"))
    except:
        kaori.send_message(msg.chat.id,"❌ Não consegui pegar thumbnail.")

# -------------------------
# /YTINFO
# -------------------------
@kaori.message_handler(commands=['ytinfo'])
def ytinfo(msg):
    query = msg.text.replace("/ytinfo","").strip()
    if not query:
        kaori.reply_to(msg, "📺 Use:\n/ytinfo link ou nome")
        return
    try:
        with yt_dlp.YoutubeDL({"quiet":True,"default_search":"ytsearch1"}) as ydl:
            info = ydl.extract_info(query, download=False)
        duration = info.get("duration")
        tempo = f"{duration//60}:{duration%60:02d}" if duration else "?"
        texto = f"🎬 {info.get('title')}\n📺 Canal: {info.get('uploader')}\n👁 Views: {info.get('view_count')}\n⏱ Duração: {tempo}"
        kaori.send_message(msg.chat.id, texto)
    except:
        kaori.send_message(msg.chat.id,"❌ Não consegui pegar informações.")

# -------------------------
# /JOKE
# -------------------------
@kaori.message_handler(commands=['joke'])
def joke(msg):
    try:
        r = requests.get("https://v2.jokeapi.dev/joke/Any?lang=pt").json()
        kaori.send_message(msg.chat.id, r.get("joke") if r["type"]=="single" else f"{r['setup']}\n{r['delivery']}")
    except:
        kaori.send_message(msg.chat.id,"❌ Erro ao buscar piada")

# -------------------------
# /FACT
# -------------------------
@kaori.message_handler(commands=['fact'])
def fact(msg):
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()
        kaori.send_message(msg.chat.id,r["text"])
    except:
        kaori.send_message(msg.chat.id,"❌ Erro ao buscar fato")

# -------------------------
# CHAT COM BOT
# -------------------------
@kaori.message_handler(func=lambda m: True, content_types=['text'])
def chat(msg):
    if msg.text.startswith("/"):
        return
    if not OPENAI_KEY:
        kaori.send_message(msg.chat.id, "❌ API do OpenAI não configurada para conversar 😢")
        return
    try:
        import openai
        openai.api_key = OPENAI_KEY
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Você é Kaori, uma assistente simpática. Responda de forma curta e amigável ao usuário: {msg.text}",
            temperature=0.7,
            max_tokens=150
        )
        kaori.send_message(msg.chat.id, response["choices"][0]["text"].strip())
    except Exception as e:
        kaori.send_message(msg.chat.id, f"❌ Erro ao conversar:\n{e}")

# -------------------------
# RUN
# -------------------------
print(f"🌻 Kaori {BOT_VERSION} iniciada")
kaori.infinity_polling()