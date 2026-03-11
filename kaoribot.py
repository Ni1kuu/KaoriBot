# kaoribot.py
import telebot
import os
import time

# Pega o token do bot da variável BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("⚠️ Token não definido! Crie uma variável BOT_TOKEN no Railway com o token do BotFather.")

bot = telebot.TeleBot(BOT_TOKEN)

# --- Comando /start ---
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🌸 Olá! Eu sou a KaoriBot!\nUse /m para ver todos os comandos."
    )

# --- Comando /menu ou /m ---
@bot.message_handler(commands=['m','menu'])
def menu(msg):
    texto = """
╭━━━━━━🌸 KAORI BOT 🌸━━━━━━╮
├ /start → Iniciar o bot
├ /m → Abrir menu de comandos
├ /ping → Ver ping do bot em ms
├ /fixar → Fixar mensagem
├ /info → Informações do bot
╰━━━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.send_message(msg.chat.id, texto)

# --- Comando /ping ---
@bot.message_handler(commands=['ping'])
def ping(msg):
    start_time = time.time()
    message = bot.send_message(msg.chat.id, "⏳ Calculando ping...")
    end_time = time.time()
    ping_ms = int((end_time - start_time) * 1000)
    bot.edit_message_text(f"🏓 Pong! Ping: {ping_ms} ms", msg.chat.id, message.message_id)

# --- Comando /fixar ---
@bot.message_handler(commands=['fixar'])
def fixar(msg):
    mensagem = bot.send_message(
        msg.chat.id,
        "📌 Mensagem fixada pela Kaori 🌸"
    )
    try:
        bot.pin_chat_message(msg.chat.id, mensagem.message_id)
    except Exception as e:
        bot.send_message(msg.chat.id, f"⚠️ Não consegui fixar: {e}")

# --- Comando /info ---
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

# --- Inicialização do bot ---
print("KaoriBot está online 🌸")
bot.infinity_polling()