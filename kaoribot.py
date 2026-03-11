import telebot
from telebot import types
import random
import time
import os

# ─── CONFIGURAÇÃO DO BOT ───
TOKEN = os.getenv("BOT_TOKEN") or "8791892359:AAHgDmGvBNBueRDm5vwdZmT9Hjj1_LGhaTI"
bot = telebot.TeleBot(TOKEN)

BOT_VERSION = "2.0"
CREATOR = "Nikuu"
start_time = time.time()

# ─── XP E NÍVEL DOS USUÁRIOS ───
user_xp = {}  # {user_id: xp}

def add_xp(user_id, amount=1):
    xp = user_xp.get(user_id,0)
    xp += amount
    user_xp[user_id] = xp
    return xp

def get_level(xp):
    return xp // 10  # cada 10 XP = 1 nível

def xp_bar(xp):
    level = get_level(xp)
    xp_in_level = xp % 10
    total_slots = 10
    filled = "█" * xp_in_level
    empty = "░" * (total_slots - xp_in_level)
    return f"[{filled}{empty}] Lvl {level}"

# ─── NÍVEL DO BOT (DEUS CÓSMICO) ───
BOT_XP = 10000
BOT_LEVEL_NAME = "🌌 DEUS CÓSMICO 🌌"
BOT_XP_BAR = "[██████████] Lvl MAX"

# ─── STATUS DO BOT ───
bot_ativo = True

# ─── MENU COMPLETO ───
def menu_text():
    return f"""
╭━━━🌸 *MENU KAORI BOT* 🌸━━━╮

👤 Usuários
/s → Criar figurinhas
/m → Abrir menu
/h → Dicas e surpresas
/i → Informações
/id → Ver seu ID
/p → Ver seu perfil
/a → Ver avatar

🎮 Diversão
/d → Número aleatório
/e → Repetir mensagem
/r → Resposta aleatória
/f → Brincadeiras (forca)
/c → Cara ou coroa
/ro → Rolar dado grande
/j → Contar piada
/q → Quiz aleatório

🛡 Administração
/pin → Fixar mensagem respondida
/unpin → Desafixar mensagem

🤖 Bot
/start → Iniciar bot
/stats → Status completo
/ping → Verificar se estou online
/up → Uptime do bot
/status → Status completo
/ativar → Ativar bot
/desativar → Desativar bot

╰━━━━━━━━━━━━━━━━━━━━╯
"""

# ─── FUNÇÕES AUXILIARES ───
def uptime():
    uptime_sec = int(time.time() - start_time)
    h = uptime_sec // 3600
    m = (uptime_sec % 3600) // 60
    s = uptime_sec % 60
    return f"{h}h {m}m {s}s"

def measure_ping(chat_id):
    start_ping = time.time()
    bot.send_chat_action(chat_id, 'typing')
    ping_ms = int((time.time() - start_ping) * 1000)
    return ping_ms

# ─── COMANDOS ───
@bot.message_handler(commands=['start'])
def start(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id,
        f"🌸 Olá {msg.from_user.first_name}!\n"
        f"Eu sou a *KaoriBot v{BOT_VERSION}*\n"
        "Use /m para ver meus comandos ✨",parse_mode="Markdown")

@bot.message_handler(commands=['m'])
def menu(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id, menu_text(),parse_mode="Markdown")

@bot.message_handler(commands=['h'])
def tips(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    dicas = ["🌸 Dica do dia: Seja paciente!", 
             "🌸 Dica do dia: Respire fundo antes de agir.", 
             "🌸 Dica do dia: Ajude alguém hoje!"]
    bot.send_message(msg.chat.id, random.choice(dicas))

@bot.message_handler(commands=['i'])
def info(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id,
                     f"🌸 KaoriBot v{BOT_VERSION}\nBot de diversão e utilidades")

@bot.message_handler(commands=['id'])
def user_id(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id,f"🆔 Seu ID: `{msg.from_user.id}`",parse_mode="Markdown")

@bot.message_handler(commands=['p'])
def perfil(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    username = msg.from_user.username
    username = "@"+username if username else "sem username"
    bot.send_message(msg.chat.id,
        f"╭━━━👤 PERFIL ━━━╮\nNome: {msg.from_user.first_name}\nUsuário: {username}\nID: {msg.from_user.id}\n╰━━━━━━━━━━━━╯",
        parse_mode="Markdown")

@bot.message_handler(commands=['a'])
def avatar(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    photos = bot.get_user_profile_photos(msg.from_user.id)
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        bot.send_photo(msg.chat.id, file_id, caption="🌸 Seu avatar")
    else:
        bot.send_message(msg.chat.id,"Você não possui foto.")

# ─── DIVERSÃO ───
@bot.message_handler(commands=['d'])
def dado(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id,f"🎲 Número aleatório: {random.randint(1,6)}")

@bot.message_handler(commands=['e'])
def echo(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    text = msg.text.replace("/e","").strip()
    if not text:
        bot.send_message(msg.chat.id,"💡 Dica: Use /e seguido do que deseja que eu repita. Ex: `/e Olá!`")
    else:
        bot.send_message(msg.chat.id,f"💬 {text}")

@bot.message_handler(commands=['r'])
def random_reply(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    respostas = ["🌸 Sim!", "🌸 Não!", "🌸 Talvez…", "🌸 Com certeza!", "🌸 Pergunte novamente."]
    bot.send_message(msg.chat.id, random.choice(respostas))

@bot.message_handler(commands=['f'])
def forca(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    palavras = ["Kaori","Bot","Telegram","Python","Railway"]
    palavra = random.choice(palavras).upper()
    bot.send_message(msg.chat.id,
        f"🎯 Palavra escolhida (demo): {palavra}\n💡 Dica: Este é um teste, tente adivinhar letras em versões futuras!")

@bot.message_handler(commands=['c'])
def coin(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id,f"🪙 {random.choice(['Cara','Coroa'])}")

@bot.message_handler(commands=['ro'])
def roll(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.send_message(msg.chat.id,f"🎲 Rolagem grande: {random.randint(1,20)}")

@bot.message_handler(commands=['j'])
def joke(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    piadas = ["🌸 Por que o gato mia? Porque está com fome!", 
              "🌸 Por que o bot foi ao médico? Porque travou!"]
    bot.send_message(msg.chat.id,random.choice(piadas))

@bot.message_handler(commands=['q'])
def quiz(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    perguntas = [
        ("🌸 Qual linguagem usamos aqui? (Python/Java)", "💡 Dica: Responda apenas com a palavra correta, ex: Python"),
        ("🌸 Qual bot você está usando? (KaoriBot/Outro)", "💡 Dica: Responda apenas com KaoriBot ou Outro")
    ]
    pergunta,dica = random.choice(perguntas)
    bot.send_message(msg.chat.id,f"{pergunta}\n{dica}")

# ─── ADMINISTRATIVO ───
@bot.message_handler(commands=['pin'])
def pin(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    if msg.reply_to_message:
        bot.pin_chat_message(msg.chat.id,msg.reply_to_message.message_id)
        bot.send_message(msg.chat.id,"📌 Mensagem fixada 🌸")

@bot.message_handler(commands=['unpin'])
def unpin(msg):
    if not bot_ativo: return
    add_xp(msg.from_user.id)
    bot.unpin_chat_message(msg.chat.id)
    bot.send_message(msg.chat.id,"📎 Todas as mensagens foram desafixadas 🌸")

# ─── STATUS COMPLETO / STATS ───
@bot.message_handler(commands=['stats','status'])
def full_stats(msg):
    if not bot_ativo: return
    user_id = msg.from_user.id
    xp = user_xp.get(user_id,0)
    bar = xp_bar(xp)
    up = uptime()
    ping_ms = measure_ping(msg.chat.id)

    text = f"""
╭━━━🌸 *KAORI BOT STATUS* 🌸━━━╮

⏱ Uptime
┃ {up}

📡 Ping
┃ {ping_ms} ms

🧠 Versão
┃ v{BOT_VERSION}

👤 Criador
┃ {CREATOR}

⭐ XP
┃ {bar}

🤖 BOT XP
┃ {BOT_XP_BAR} {BOT_LEVEL_NAME}

╰━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.send_message(msg.chat.id,text,parse_mode="Markdown")
    add_xp(user_id)

# ─── ATIVAR / DESATIVAR BOT ───
@bot.message_handler(commands=['ativar'])
def ativar_bot(msg):
    global bot_ativo
    bot_ativo = True
    bot.send_message(msg.chat.id,"🌸 KaoriBot foi ativada!")

@bot.message_handler(commands=['desativar'])
def desativar_bot(msg):
    global bot_ativo
    bot_ativo = False
    bot.send_message(msg.chat.id,"🌸 KaoriBot foi desativada!")

# ─── BOAS-VINDAS AUTOMÁTICAS ───
@bot.message_handler(content_types=['new_chat_members'])
def welcome(msg):
    if not bot_ativo: return
    for user in msg.new_chat_members:
        add_xp(user.id)
        bot.send_message(msg.chat.id,
            f"🌸 Bem-vindo(a) {user.first_name}!\n"
            "Seja bem-vindo(a) ao grupo da KaoriBot 🧩✨\n"
            "Digite /m para ver meus comandos."
        )
        try:
            photos = bot.get_user_profile_photos(user.id)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                bot.send_photo(msg.chat.id, file_id, caption=f"🌸 Este é você, {user.first_name}!")
        except:
            pass

# ─── INICIAR BOT ───
print("🌸✨ KaoriBot v2.4 está online! ✨🌸\n"
      "🧩 Pronta para diversão, figurinhas e surpresas!\n"
      "💌 Use /m para ver todos os meus comandos fofinhos!")
bot.infinity_polling()