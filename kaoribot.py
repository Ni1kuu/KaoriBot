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
OWM_KEY = os.getenv("OPENWEATHER_KEY")
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
/envgif → vídeo ou foto para sticker/gif
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
# STICKER / ENVGIF
# -------------------------
@kaori.message_handler(content_types=['photo','video'])
def sticker(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        if msg.content_type == "photo":
            file_info = kaori.get_file(msg.photo[-1].file_id)
            ext = "png"
        else:
            file_info = kaori.get_file(msg.video.file_id)
            ext = "mp4"
        downloaded = kaori.download_file(file_info.file_path)
        with open(f"temp/input.{ext}","wb") as f:
            f.write(downloaded)
        if ext=="png":
            img = Image.open("temp/input.png").convert("RGBA")
            img.thumbnail((512,512))
            img.save("temp/sticker.webp","WEBP")
            with open("temp/sticker.webp","rb") as s:
                kaori.send_sticker(msg.chat.id,s)
        else:
            kaori.send_message(msg.chat.id,"⚠️ Conversão de vídeo para gif disponível no /envgif comando")
    except Exception as e:
        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# -------------------------
# /ENVGIF (video to gif)
# -------------------------
@kaori.message_handler(commands=['envgif'])
def envgif(msg):
    if not msg.reply_to_message or not msg.reply_to_message.video:
        kaori.reply_to(msg,"Responda a um vídeo para converter em gif")
        return
    try:
        file_info = kaori.get_file(msg.reply_to_message.video.file_id)
        downloaded = kaori.download_file(file_info.file_path)
        os.makedirs("temp", exist_ok=True)
        path_in = "temp/input.mp4"
        path_out = "temp/output.gif"
        with open(path_in,"wb") as f:
            f.write(downloaded)
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(path_in)
        clip.write_gif(path_out)
        with open(path_out,"rb") as g:
            kaori.send_document(msg.chat.id,g)
    except Exception as e:
        kaori.send_message(msg.chat.id,f"❌ Erro: {e}")

# -------------------------
# /CLIMA
# -------------------------
@kaori.message_handler(commands=['clima'])
def clima(msg):
    if not OWM_KEY:
        kaori.send_message(msg.chat.id,"❌ API key do OpenWeather não configurada")
        return
    query = msg.text.replace("/clima","").strip()
    if not query:
        kaori.reply_to(msg,"Use:\n/clima cidade")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={OWM_KEY}&units=metric&lang=pt"
    try:
        r = requests.get(url).json()
        kaori.send_message(msg.chat.id,
            f"🌤 {r['name']} - {r['weather'][0]['description'].capitalize()}\n🌡 Temperatura: {r['main']['temp']}°C\n💨 Vento: {r['wind']['speed']} m/s")
    except:
        kaori.send_message(msg.chat.id,"❌ Cidade não encontrada")

# -------------------------
# /LYRICS
# -------------------------
@kaori.message_handler(commands=['lyrics'])
def lyrics(msg):
    if not GENIUS_KEY:
        kaori.send_message(msg.chat.id,"❌ API key do Genius não configurada")
        return
    query = msg.text.replace("/lyrics","").strip()
    if not query:
        kaori.reply_to(msg,"Use:\n/lyrics nome da música")
        return
    try:
        headers = {"Authorization": f"Bearer {GENIUS_KEY}"}
        search_url = f"https://api.genius.com/search?q={query}"
        r = requests.get(search_url, headers=headers).json()
        hits = r["response"]["hits"]
        if not hits:
            kaori.send_message(msg.chat.id,"❌ Música não encontrada")
            return
        lyrics_path = hits[0]["result"]["path"]
        song_url = f"https://genius.com{lyrics_path}"
        kaori.send_message(msg.chat.id,f"🎵 {hits[0]['result']['title']}\n🔗 {song_url}")
    except:
        kaori.send_message(msg.chat.id,"❌ Erro ao buscar letra")

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
        thumb = info.get("thumbnail")
        duration = info.get("duration")
        tempo = f"{duration//60}:{duration%60:02d}" if duration else "desconhecido"
        if thumb:
            kaori.send_photo(msg.chat.id, thumb, caption=f"🎵 {title}\n⏱ {tempo}")
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
# RUN
# -------------------------
print("🌻 Kaori 2.6.1 iniciada")
kaori.infinity_polling()