import telebot
import os
import time
import requests
import urllib.parse
from PIL import Image
import io

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("⚠️ Token não definido! Crie uma variável BOT_TOKEN no Railway.")

bot = telebot.TeleBot(BOT_TOKEN)

# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🌸 Olá! Eu sou a KaoriBot!\nUse /menu para ver meus comandos."
    )

# =========================
# MENU
# =========================
@bot.message_handler(commands=['menu'])
def menu(msg):

    texto = """
╭━━━━━━━━━━━━━━━🌸 KAORI BOT 🌸━━━━━━━━━━━━━━━╮

👤 Usuário
├ /start → Iniciar o bot
├ /ping → Ver ping do bot
├ /id → Ver seu ID
├ /avatar → Ver sua foto de perfil

🌐 Utilidades
├ /google → Pesquisar na web
├ /fig → Criar figurinha (envie foto com /fig)
├ /info → Informações do bot

🛡 Moderação
├ /fixar → Fixar mensagem (responda)
├ /desfixar → Remover mensagem fixada

╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""

    bot.send_message(msg.chat.id, texto)

# =========================
# PING
# =========================
@bot.message_handler(commands=['ping'])
def ping(msg):

    inicio = time.time()

    mensagem = bot.send_message(msg.chat.id, "🏓 Pong!")

    fim = time.time()

    ms = int((fim - inicio) * 1000)

    bot.edit_message_text(
        f"🏓 Pong!\n⏱ Ping: {ms} ms",
        msg.chat.id,
        mensagem.message_id
    )

# =========================
# ID
# =========================
@bot.message_handler(commands=['id'])
def id_usuario(msg):

    texto = f"""
🆔 Informações

👤 Seu ID: {msg.from_user.id}
💬 Chat ID: {msg.chat.id}
"""

    bot.send_message(msg.chat.id, texto)

# =========================
# AVATAR
# =========================
@bot.message_handler(commands=['avatar'])
def avatar(msg):

    try:

        fotos = bot.get_user_profile_photos(msg.from_user.id)

        if fotos.total_count == 0:
            bot.send_message(msg.chat.id, "⚠️ Você não tem foto de perfil.")
            return

        file_id = fotos.photos[0][-1].file_id

        bot.send_photo(
            msg.chat.id,
            file_id,
            caption="🖼 Seu avatar"
        )

    except Exception as e:

        bot.send_message(msg.chat.id, f"Erro ao pegar avatar: {e}")

# =========================
# GOOGLE
# =========================
@bot.message_handler(commands=['google'])
def google(msg):

    try:

        texto = msg.text.replace("/google", "").strip()

        if texto == "":
            bot.send_message(msg.chat.id, "Use:\n/google assunto")
            return

        query = urllib.parse.quote(texto)

        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        r = requests.get(url).json()

        resposta = f"🔎 Pesquisa: {texto}\n\n"

        if r.get("AbstractURL"):
            resposta += f"🌐 {r['AbstractURL']}\n"

        if r.get("RelatedTopics"):
            for i in r["RelatedTopics"][:3]:
                if "FirstURL" in i:
                    resposta += f"🔗 {i['FirstURL']}\n"

        if resposta.strip() == f"🔎 Pesquisa: {texto}":
            resposta += f"https://www.google.com/search?q={query}"

        bot.send_message(msg.chat.id, resposta)

    except Exception as e:

        bot.send_message(msg.chat.id, f"Erro na pesquisa: {e}")

# =========================
# FIXAR
# =========================
@bot.message_handler(commands=['fixar'])
def fixar(msg):

    if msg.reply_to_message:

        try:

            bot.pin_chat_message(
                msg.chat.id,
                msg.reply_to_message.message_id
            )

            bot.send_message(msg.chat.id, "📌 Mensagem fixada!")

        except Exception as e:

            bot.send_message(msg.chat.id, f"Erro ao fixar: {e}")

    else:

        bot.send_message(msg.chat.id, "Responda a mensagem que deseja fixar.")

# =========================
# DESFIXAR
# =========================
@bot.message_handler(commands=['desfixar'])
def desfixar(msg):

    try:

        bot.unpin_all_chat_messages(msg.chat.id)

        bot.send_message(msg.chat.id, "📌❌ Mensagem desfixada!")

    except Exception as e:

        bot.send_message(msg.chat.id, f"Erro: {e}")

# =========================
# FIGURINHA
# =========================
@bot.message_handler(content_types=['photo'])
def figurinha(msg):

    if msg.caption and msg.caption.lower() == "/fig":

        try:

            file_id = msg.photo[-1].file_id

            file_info = bot.get_file(file_id)

            downloaded_file = bot.download_file(file_info.file_path)

            image = Image.open(io.BytesIO(downloaded_file)).convert("RGBA")

            max_size = 512

            width, height = image.size

            ratio = min(max_size / width, max_size / height)

            new_width = int(width * ratio)
            new_height = int(height * ratio)

            image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            final = Image.new("RGBA", (512, 512), (0,0,0,0))

            final.paste(
                image,
                ((512-new_width)//2, (512-new_height)//2),
                image
            )

            bio = io.BytesIO()
            bio.name = "sticker.png"

            final.save(bio, "PNG")
            bio.seek(0)

            bot.send_sticker(msg.chat.id, bio)

        except Exception as e:

            bot.send_message(msg.chat.id, f"Erro ao criar figurinha: {e}")

# =========================
# INFO
# =========================
@bot.message_handler(commands=['info'])
def info(msg):

    bot.send_message(
        msg.chat.id,
        "🌸 KaoriBot\n\nBot de utilidades do Telegram.\nRodando com pyTelegramBotAPI."
    )

# =========================
# INICIAR BOT
# =========================
print("KaoriBot está online 🌸")

bot.infinity_polling(skip_pending=True)