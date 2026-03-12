import telebot
import os
import time
import requests
import urllib.parse
from PIL import Image
import io
import random

# =========================
# Configurações
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXABAY_KEY = os.getenv("PIXABAY_API_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")
BOT_CREATOR = "@seu_username_aqui"

if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN não definido no Railway.")
if not PIXABAY_KEY:
    raise ValueError("⚠️ PIXABAY_API_KEY não definido no Railway.")
if not HUGGINGFACE_KEY:
    raise ValueError("⚠️ HUGGINGFACE_KEY não definido no Railway.")

kaori = telebot.TeleBot(BOT_TOKEN)
start_time = time.time()  # tempo de início do bot

# =========================
# /start
# =========================
@kaori.message_handler(commands=['start'])
def start(msg):
    texto = """
╭━━━━━━━━━━━━━━━🌻 BEM-VINDO(A) AO KAORI 🌻━━━━━━━━━━━━━━━╮
✨ "Olá, viajante do Telegram! ✨

Hoje é um dia perfeito para explorar, se divertir e descobrir coisas mágicas.
Aqui você pode criar figurinhas, gerar imagens incríveis, buscar fotos legais,
brincar com comandos divertidos e muito mais! 💖

Não se esqueça: cada comando é uma pequena aventura,
e Kaori está aqui para te guiar com fofura e alegria! 🌻

Para começar, use o comando /menu e veja tudo o que podemos fazer juntos! 🎀
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# =========================
# /menu
# =========================
@kaori.message_handler(commands=['menu'])
def menu(msg):
    texto = """
╭━━━━━━━━━━━━━━━🌻 KAORI 🌻━━━━━━━━━━━━━━━╮

👤 Usuário
├ /start → Mensagem de boas-vindas
├ /ping → Ver ping em ms
├ /id → Ver seu ID
├ /avatar → Ver sua foto de perfil

🌐 Utilidades
├ /google → Pesquisar na web
├ /img → Buscar imagens (Pixabay)
├ /aiimg → Criar imagens IA seguras
├ /fig → Criar figurinha
├ /info → Informações do bot

🛡 Moderação
├ /fixar → Fixar mensagem (responda a mensagem)
├ /desfixar → Desafixar mensagem

╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    kaori.send_message(msg.chat.id, texto)

# =========================
# /ping
# =========================
@kaori.message_handler(commands=['ping'])
def ping(msg):
    inicio = time.time()
    mensagem = kaori.send_message(msg.chat.id, "🏓 Pong!")
    fim = time.time()
    ms = int((fim - inicio) * 1000)
    kaori.edit_message_text(
        f"🏓 Pong!\n⏱ Ping: {ms} ms",
        msg.chat.id,
        mensagem.message_id
    )

# =========================
# /id
# =========================
@kaori.message_handler(commands=['id'])
def id_usuario(msg):
    texto = f"🆔 Seu ID: {msg.from_user.id}\n💬 Chat ID: {msg.chat.id}"
    kaori.send_message(msg.chat.id, texto)

# =========================
# /avatar
# =========================
@kaori.message_handler(commands=['avatar'])
def avatar(msg):
    try:
        fotos = kaori.get_user_profile_photos(msg.from_user.id)
        if fotos.total_count == 0:
            kaori.send_message(msg.chat.id, "⚠️ Você não tem foto de perfil.")
            return
        file_id = fotos.photos[0][-1].file_id
        kaori.send_photo(msg.chat.id, file_id, caption="🖼 Seu avatar")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"Erro ao pegar avatar: {e}")

# =========================
# /google
# =========================
@kaori.message_handler(commands=['google'])
def google(msg):
    texto = msg.text.replace("/google", "").strip()
    if not texto:
        kaori.send_message(msg.chat.id, "Use:\n/google <termo de pesquisa>")
        return
    query = urllib.parse.quote(texto)
    link = f"https://www.google.com/search?q={query}"
    kaori.send_message(msg.chat.id, f"🔎 Pesquisa no Google:\n{link}")

# =========================
# /img (Pixabay)
# =========================
@kaori.message_handler(commands=['img'])
def img(msg):
    texto = msg.text.replace("/img", "").strip()
    if not texto:
        kaori.send_message(msg.chat.id, "Use:\n/img <termo>")
        return
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={texto}&image_type=photo&per_page=50"
    r = requests.get(url).json()
    if r['totalHits'] == 0:
        kaori.send_message(msg.chat.id, "⚠️ Nenhuma imagem encontrada.")
        return
    img_url = r['hits'][random.randint(0, len(r['hits'])-1)]['largeImageURL']
    r_img = requests.get(img_url)
    foto_bytes = io.BytesIO(r_img.content)
    foto_bytes.name = "img.jpg"
    foto_bytes.seek(0)
    kaori.send_photo(msg.chat.id, foto_bytes, caption=f"🖼 Resultado para: {texto}")

# =========================
# /aiimg (Hugging Face Stable Diffusion)
# =========================
@kaori.message_handler(commands=['aiimg'])
def aiimg(msg):
    texto = msg.text.replace("/aiimg", "").strip()
    if not texto:
        kaori.send_message(msg.chat.id, "Use:\n/aiimg <descrição da imagem>")
        return

    aguardando = kaori.send_message(msg.chat.id, "🌻 Gerando sua imagem IA...")

    try:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_KEY}"
        }
        payload = {"inputs": texto, "options":{"use_gpu": True}}
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        if r.status_code == 200:
            img_bytes = r.content
            foto = io.BytesIO(img_bytes)
            foto.name = "aiimg.png"
            foto.seek(0)
            kaori.send_photo(msg.chat.id, foto, caption=f"🖼 Imagem IA: {texto}")
            kaori.edit_message_text("🌻 Imagem gerada com sucesso!", msg.chat.id, aguardando.message_id)
        else:
            kaori.edit_message_text(
                f"⚠️ Não foi possível gerar imagem (status {r.status_code})",
                msg.chat.id,
                aguardando.message_id
            )

    except Exception as e:
        kaori.edit_message_text(f"⚠️ Erro ao gerar imagem: {e}", msg.chat.id, aguardando.message_id)

# =========================
# /fixar
# =========================
@kaori.message_handler(commands=['fixar'])
def fixar(msg):
    if msg.reply_to_message:
        try:
            kaori.pin_chat_message(msg.chat.id, msg.reply_to_message.message_id)
            kaori.send_message(msg.chat.id, "📌 Mensagem fixada!")
        except Exception as e:
            kaori.send_message(msg.chat.id, f"Erro ao fixar: {e}")
    else:
        kaori.send_message(msg.chat.id, "Responda a mensagem que deseja fixar.")

# =========================
# /desfixar
# =========================
@kaori.message_handler(commands=['desfixar'])
def desfixar(msg):
    try:
        kaori.unpin_all_chat_messages(msg.chat.id)
        kaori.send_message(msg.chat.id, "📌❌ Mensagem desfixada!")
    except Exception as e:
        kaori.send_message(msg.chat.id, f"Erro: {e}")

# =========================
# Figurinhas automáticas (qualquer imagem)
# =========================
@kaori.message_handler(content_types=['photo'])
def figurinha(msg):
    try:
        file_id = msg.photo[-1].file_id
        file_info = kaori.get_file(file_id)
        downloaded_file = kaori.download_file(file_info.file_path)
        image = Image.open(io.BytesIO(downloaded_file)).convert("RGBA")
        max_size = 512
        width, height = image.size
        ratio = min(max_size / width, max_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        final = Image.new("RGBA", (512, 512), (0,0,0,0))
        final.paste(image, ((512-new_width)//2, (512-new_height)//2), image)
        bio = io.BytesIO()
        bio.name = "sticker.png"
        final.save(bio, "PNG")
        bio.seek(0)
        kaori.send_sticker(msg.chat.id, bio)
    except Exception as e:
        kaori.send_message(msg.chat.id, f"Erro ao criar figurinha: {e}")

# =========================
# /info
# =========================
@kaori.message_handler(commands=['info'])
def info(msg):
    uptime_seconds = int(time.time() - start_time)
    horas = uptime_seconds // 3600
    minutos = (uptime_seconds % 3600) // 60
    segundos = uptime_seconds % 60

    texto = f"""
🌻 Kaori v1.8.3 🌻
Breve biografia: Sou um bot divertido para Telegram, ajudando com figurinhas, imagens, buscas e comandos fofos! 💖
Criador: {BOT_CREATOR}
Tempo online: {horas}h {minutos}m {segundos}s
"""
    kaori.send_message(msg.chat.id, texto)

# =========================
# Iniciar Kaori
# =========================
print("Kaori v1.8.3 está online 🌻")
kaori.infinity_polling(skip_pending=True)