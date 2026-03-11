# kaoribot.py
import telebot
import os
import time
from PIL import Image
import io

# Pega token do Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("⚠️ Token não definido! Crie uma variável BOT_TOKEN no Railway.")

bot = telebot.TeleBot(BOT_TOKEN)

# --- Lista de comandos para menu automático ---
COMMANDS_INFO = {}

def register_command(name, description):
    """Registra comando no menu automaticamente"""
    COMMANDS_INFO[name] = description

# --- /start ---
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "🌸 Olá! Eu sou a KaoriBot!\nUse /menu para ver todos os comandos.")
register_command('start', 'Iniciar o bot')

# --- /menu (menu fofo reformulado) ---
@bot.message_handler(commands=['menu'])
def menu(msg):
    texto = f"""
╭━━━━━━━━━━━━━━━🌸 KAORI BOT 🌸━━━━━━━━━━━━━━━╮
👤 Usuário
├ /start → Iniciar o bot
├ /ping → Ver ping do bot
├ /fixar → Fixar mensagem (responda a mensagem)
├ /info → Informações do bot
├ /fig → Criar figurinha ꒰ᐢ. .ᐢ꒱₊˚⊹
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.send_message(msg.chat.id, texto)
register_command('menu', 'Abrir menu completo fofo')

# --- /ping ---
@bot.message_handler(commands=['ping'])
def ping(msg):
    start_time = time.time()
    bot.send_message(msg.chat.id, "🏓 Pong! Kaori está online 🌸")
    end_time = time.time()
    ping_ms = int((end_time - start_time) * 1000)
    bot.send_message(msg.chat.id, f"⏱ Ping aproximado: {ping_ms} ms")
register_command('ping', 'Ver ping do bot')

# --- /fixar ---
@bot.message_handler(commands=['fixar'])
def fixar(msg):
    if msg.reply_to_message:
        try:
            bot.pin_chat_message(msg.chat.id, msg.reply_to_message.message_id)
            bot.send_message(msg.chat.id, "📌 Mensagem fixada com sucesso! 🌸")
        except Exception as e:
            bot.send_message(msg.chat.id, f"⚠️ Não consegui fixar: {e}")
    else:
        bot.send_message(msg.chat.id, "⚠️ Para fixar, responda a mensagem que quer fixar com /fixar")
register_command('fixar', 'Fixar mensagem (responda a mensagem)')

# --- /info ---
@bot.message_handler(commands=['info'])
def info(msg):
    texto = f"""
🌸 KaoriBot Info:

Versão: 1.0
Criador: Você
Hospedagem: Railway
Biblioteca: pyTelegramBotAPI

Rostinho fofo: ꒰ᐢ. .ᐢ꒱₊˚⊹
"""
    bot.send_message(msg.chat.id, texto)
register_command('info', 'Informações do bot')

# --- /fig para criar figurinhas de qualquer tamanho ---
@bot.message_handler(content_types=['photo'])
def foto_para_figura(msg):
    if msg.caption and msg.caption.lower() == "/fig":
        try:
            file_id = msg.photo[-1].file_id  # maior resolução
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Abre a imagem com Pillow
            image = Image.open(io.BytesIO(downloaded_file)).convert("RGBA")

            # Redimensiona mantendo proporção
            max_size = 512
            width, height = image.size
            ratio = min(max_size / width, max_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            # Substituído ANTIALIAS por LANCZOS para Pillow 10+
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Cria canvas 512x512 com fundo transparente
            final_image = Image.new("RGBA", (512, 512), (0,0,0,0))
            final_image.paste(image, ((512 - new_width) // 2, (512 - new_height) // 2), image)

            # Salva em memória
            bio = io.BytesIO()
            bio.name = "sticker.png"
            final_image.save(bio, "PNG")
            bio.seek(0)

            # Envia como figurinha
            bot.send_sticker(msg.chat.id, bio)

        except Exception as e:
            bot.send_message(msg.chat.id, f"⚠️ Erro ao criar figurinha: {e}")

register_command('fig', 'Criar figurinha a partir de imagem (qualquer tamanho, use /fig na legenda)')

# --- Inicialização ---
print("KaoriBot está online 🌸")
bot.infinity_polling()