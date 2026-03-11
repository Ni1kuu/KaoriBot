# kaoribot.py
import telebot
import os
import time

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
    bot.send_message(msg.chat.id, "🌸 Olá! Eu sou a KaoriBot!\nUse /m para ver todos os comandos.")
register_command('start', 'Iniciar o bot')

# --- /m /menu ---
@bot.message_handler(commands=['m','menu'])
def menu(msg):
    texto = "╭━━━━━━🌸 KAORI BOT 🌸━━━━━━╮\n"
    for cmd, desc in COMMANDS_INFO.items():
        texto += f"├ /{cmd} → {desc}\n"
    texto += "╰━━━━━━━━━━━━━━━━━━━━━━╯"
    bot.send_message(msg.chat.id, texto)
register_command('m', 'Abrir menu de comandos')
register_command('menu', 'Abrir menu de comandos')

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
    texto = """
🌸 KaoriBot Info:

Versão: 1.0
Criador: Você
Hospedagem: Railway
Biblioteca: pyTelegramBotAPI
"""
    bot.send_message(msg.chat.id, texto)
register_command('info', 'Informações do bot')

# --- Exemplo de comando extra ---
@bot.message_handler(commands=['hello'])
def hello(msg):
    bot.send_message(msg.chat.id, "Olá! 🌸 Comando extra funcionando!")
register_command('hello', 'Teste de novo comando')

# --- Inicialização ---
print("Kaori está online! ꒰ᐢ. .ᐢ꒱₊˚⊹ 🌸")
bot.infinity_polling()