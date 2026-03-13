import os
import time
import telebot
import requests
import yt_dlp
from PIL import Image
import wikipedia
from io import BytesIO

# -------------------------
# VARIÁVEIS
# -------------------------

TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
BOT_VERSION = "2.4"
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
/wiki termo

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

🌤 Clima
/clima cidade → clima da cidade

🧠 IA
/ai → resposta estilo IA

🖼 Figurinhas
envie imagem

😂 Diversão
/joke
/fact

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
# GOOGLE
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
# PIXABAY
# -------------------------
@kaori.message_handler(commands=['img'])
def img(msg):
    query = msg.text.replace("/img", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/img imagem")
        return
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo"
    r = requests.get(url).json()
    if r["hits"]:
        kaori.send_photo(msg.chat.id, r["hits"][0]["largeImageURL"])
    else:
        kaori.send_message(msg.chat.id, "❌ Nenhuma imagem")

# -------------------------
# WIKI
# -------------------------
@kaori.message_handler(commands=['wiki'])
def wiki(msg):
    query = msg.text.replace("/wiki", "").strip()
    if not query:
        kaori.reply_to(msg, "Use:\n/wiki termo")
        return
    try:
        summary = wikipedia.summary(query, sentences=3)
        kaori.send_message(msg.chat.id, f"🌻 {summary}")
    except:
        kaori.send_message(msg.chat.id, "❌ Não encontrei")

# -------------------------
# JOKE
# -------------------------
@kaori.message_handler(commands=['joke'])
def joke(msg):
    try:
        r = requests.get("https://v2.jokeapi.dev/joke/Any?lang=pt").json()
        if r["type"] == "single":
            kaori.send_message(msg.chat.id, r["joke"])
        else:
            kaori.send_message(msg.chat.id, f"{r['setup']}\n{r['delivery']}")
    except:
        kaori.send_message(msg.chat.id, "Erro ao buscar piada")

# -------------------------
# FACT
# -------------------------
@kaori.message_handler(commands=['fact'])
def fact(msg):
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=pt").json()
        kaori.send_message(msg.chat.id, r["text"])
    except:
        kaori.send_message(msg.chat.id, "Erro ao buscar fato")

# -------------------------
# STICKER
# -------------------------
@kaori.message_handler(content_types=['photo'])
def sticker(msg):
    try:
        os.makedirs("temp", exist_ok=True)
        file_info = kaori.get_file(msg.photo[-1].file_id)
        downloaded = kaori.download_file(file_info.file_path)
        with open("temp/img.png","wb") as f:
            f.write(downloaded)
        img = Image.open("temp/img.png").convert("RGBA")
        img.thumbnail((512,512))
        img.save("temp/sticker.webp","WEBP")
        with open("temp/sticker.webp","rb") as s:
            kaori.send_sticker(msg.chat.id,s)
    except Exception as e:
        kaori.send_message(msg.chat.id,f"Erro:\n{e}")

# -------------------------
# /PLAY música com yt-dlp
# -------------------------
@kaori.message_handler(commands=['play'])
def play(msg):
    import os, yt_dlp, time
    query = msg.text.replace("/play", "").strip()
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
            "extractor_args": {"youtube": {"player_client": ["android"]}},
            "http_headers": {"User-Agent": "com.google.android.youtube/17.31.35 (Linux; U; Android 11)"},
            "default_search": "ytsearch",
            "postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "mp3","preferredquality": "192"}]
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
        if duration:
            minutos = duration // 60
            segundos = duration % 60
            tempo = f"{minutos}:{segundos:02d}"
        else:
            tempo = "desconhecido"
        if thumb:
            kaori.send_photo(msg.chat.id, thumb, caption=f"🎵 {title}\n⏱ {tempo}")
        with open(filename, "rb") as audio:
            kaori.send_audio(msg.chat.id, audio, title=title)
        kaori.edit_message_text(f"🎵 Tocando: {title}", msg.chat.id, status.message_id)
    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao baixar música:\n{e}", msg.chat.id, status.message_id)

# -------------------------
# /YTTHUMB thumbnail
# -------------------------
@kaori.message_handler(commands=['ytthumb'])
def ytthumb(msg):
    import yt_dlp
    query = msg.text.replace("/ytthumb", "").strip()
    if not query:
        kaori.reply_to(msg, "📸 Use:\n/ytthumb link ou nome")
        return
    try:
        ydl_opts = {"quiet": True, "default_search": "ytsearch1"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
        thumb = info.get("thumbnail")
        title = info.get("title")
        kaori.send_photo(msg.chat.id, thumb, caption=f"📸 {title}")
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar thumbnail.")

# -------------------------
# /YTINFO informações
# -------------------------
@kaori.message_handler(commands=['ytinfo'])
def ytinfo(msg):
    import yt_dlp
    query = msg.text.replace("/ytinfo", "").strip()
    if not query:
        kaori.reply_to(msg, "📺 Use:\n/ytinfo link ou nome")
        return
    try:
        ydl_opts = {"quiet": True, "default_search": "ytsearch1"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
        title = info.get("title")
        channel = info.get("uploader")
        views = info.get("view_count")
        duration = info.get("duration")
        if duration:
            minutos = duration // 60
            segundos = duration % 60
            tempo = f"{minutos}:{segundos:02d}"
        else:
            tempo = "?"
        texto = f"""
🎬 {title}

📺 Canal: {channel}
👁 Views: {views}
⏱ Duração: {tempo}
"""
        kaori.send_message(msg.chat.id, texto)
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar informações.")

# -------------------------
# /LYRICS letra da música
# -------------------------
@kaori.message_handler(commands=['lyrics'])
def lyrics(msg):
    import lyricsgenius
    query = msg.text.replace("/lyrics", "").strip()
    if not query:
        kaori.reply_to(msg, "🎵 Use:\n/lyrics nome da música")
        return
    try:
        GENIUS_KEY = os.getenv("GENIUS_KEY")
        genius = lyricsgenius.Genius(GENIUS_KEY)
        song = genius.search_song(query)
        if song:
            kaori.send_message(msg.chat.id, f"🎶 {song.title}:\n\n{song.lyrics}")
        else:
            kaori.send_message(msg.chat.id, "❌ Não encontrei a letra.")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"⚠️ Erro ao buscar letra:\n{e}")

# -------------------------
# /ANIME imagem aleatória
# -------------------------
@kaori.message_handler(commands=['anime'])
def anime(msg):
    try:
        url = "https://api.waifu.pics/sfw/waifu"
        r = requests.get(url).json()
        kaori.send_photo(msg.chat.id, r["url"])
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar imagem.")

# -------------------------
# /MEME meme aleatório
# -------------------------
@kaori.message_handler(commands=['meme'])
def meme(msg):
    try:
        url = "https://meme-api.com/gimme"
        r = requests.get(url).json()
        kaori.send_photo(msg.chat.id, r["url"], caption=r["title"])
    except:
        kaori.send_message(msg.chat.id, "❌ Não consegui pegar meme.")

# -------------------------
# /CLIMA cidade
# -------------------------
@kaori.message_handler(commands=['clima'])
def clima(msg):
    query = msg.text.replace("/clima", "").strip()
    if not query:
        kaori.reply_to(msg, "🌤 Use:\n/clima cidade")
        return
    try:
        OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={OPENWEATHER_KEY}&lang=pt&units=metric").json()
        if r.get("main"):
            temp = r["main"]["temp"]
            desc = r["weather"][0]["description"]
            kaori.send_message(msg.chat.id, f"🌤 Clima em {query}:\nTemperatura: {temp}°C\nDescrição: {desc}")
        else:
            kaori.send_message(msg.chat.id, "❌ Cidade não encontrada.")
    except:
        kaori.send_message(msg.chat.id, "⚠️ Erro ao buscar clima.")

# -------------------------
# /AI resposta estilo IA
# -------------------------
@kaori.message_handler(commands=['ai'])
def ai(msg):
    query = msg.text.replace("/ai", "").strip()
    if not query:
        kaori.reply_to(msg, "🧠 Use:\n/ai sua pergunta")
        return
    try:
        import openai
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":query}]
        )
        answer = response.choices[0].message.content
        kaori.send_message(msg.chat.id, f"🧠 {answer}")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"⚠️ Erro ao processar IA:\n{e}")

# -------------------------
# RUN
# -------------------------
print("🌻 Kaori iniciada")
kaori.infinity_polling()