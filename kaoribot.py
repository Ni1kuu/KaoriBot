import telebot
from telebot import types
import random
import time
import os

# TOKEN (Railway ou local)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    TOKEN = "8791892359:AAHgDmGvBNBueRDm5vwdZmT9Hjj1_LGhaTI"

bot = telebot.TeleBot(TOKEN)

start_time = time.time()

# comandos do menu do telegram
bot.set_my_commands([
types.BotCommand("s","Criar figurinhas"),
types.BotCommand("m","Abrir menu"),
types.BotCommand("h","Dicas e surpresas"),
types.BotCommand("i","Informações sobre mim"),
types.BotCommand("id","Ver seu ID"),
types.BotCommand("p","Ver seu perfil"),
types.BotCommand("a","Ver avatar"),
types.BotCommand("d","Número aleatório"),
types.BotCommand("e","Repetir mensagem"),
types.BotCommand("r","Resposta aleatória"),
types.BotCommand("f","Brincadeiras"),
types.BotCommand("c","Cara ou coroa"),
types.BotCommand("ro","Rolar dado"),
types.BotCommand("j","Contar piada"),
types.BotCommand("q","Quiz"),
types.BotCommand("pin","Fixar mensagem"),
types.BotCommand("unpin","Desafixar mensagem"),
types.BotCommand("stats","Estatísticas"),
types.BotCommand("ping","Status do bot"),
types.BotCommand("up","Uptime")
])

# MENU
def menu():
    return """
🌸 MENU DA KAORI

👤 Usuários
/s Criar figurinhas
/m Abrir menu
/h Dicas
/i Informações
/id Ver ID
/p Perfil
/a Avatar

🎮 Diversão
/d Número aleatório
/e Repetir
/r Resposta aleatória
/f Brincadeiras
/c Cara ou coroa
/ro Rolar dado
/j Piada
/q Quiz

🛡 Administração
/pin Fixar mensagem
/unpin Desafixar

🤖 Bot
/start Iniciar
/stats Estatísticas
/ping Status
/up Uptime
"""

# START
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,"🌸 Olá! Eu sou a KaoriBot\nUse /m para ver o menu")

# MENU
@bot.message_handler(commands=['m'])
def menu_cmd(msg):
    bot.send_message(msg.chat.id,menu())

# INFO
@bot.message_handler(commands=['i'])
def info(msg):
    bot.send_message(msg.chat.id,"🌸 KaoriBot\nBot de utilidades e diversão")

# ID
@bot.message_handler(commands=['id'])
def user_id(msg):
    bot.send_message(msg.chat.id,f"Seu ID: {msg.from_user.id}")

# PERFIL
@bot.message_handler(commands=['p'])
def perfil(msg):

    username = msg.from_user.username

    if username:
        username = "@"+username
    else:
        username = "sem username"

    bot.send_message(msg.chat.id,
    f"Nome: {msg.from_user.first_name}\nUsuário: {username}")

# AVATAR
@bot.message_handler(commands=['a'])
def avatar(msg):

    photos = bot.get_user_profile_photos(msg.from_user.id)

    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        bot.send_photo(msg.chat.id,file_id)
    else:
        bot.send_message(msg.chat.id,"Você não tem foto")

# RANDOM
@bot.message_handler(commands=['d'])
def dado(msg):
    bot.send_message(msg.chat.id,f"🎲 {random.randint(1,6)}")

# ECHO
@bot.message_handler(commands=['e'])
def echo(msg):
    text = msg.text.replace("/e","")
    bot.send_message(msg.chat.id,text)

# RESPOSTA
@bot.message_handler(commands=['r'])
def resposta(msg):

    respostas=[
    "Sim",
    "Não",
    "Talvez",
    "Com certeza",
    "Pergunte novamente"
    ]

    bot.send_message(msg.chat.id,random.choice(respostas))

# BRINCADEIRA
@bot.message_handler(commands=['f'])
def forca(msg):

    palavras=["python","telegram","kaori","bot"]

    palavra=random.choice(palavras)

    bot.send_message(msg.chat.id,f"Palavra da forca: {palavra}")

# CARA OU COROA
@bot.message_handler(commands=['c'])
def coin(msg):

    bot.send_message(msg.chat.id,
    random.choice(["Cara","Coroa"]))

# ROLL
@bot.message_handler(commands=['ro'])
def roll(msg):

    bot.send_message(msg.chat.id,
    f"🎲 {random.randint(1,20)}")

# PIADA
@bot.message_handler(commands=['j'])
def piada(msg):

    jokes=[
    "Programador não dorme, ele compila sonhos",
    "Bug não é erro, é feature",
    "Python > todas as linguagens"
    ]

    bot.send_message(msg.chat.id,random.choice(jokes))

# QUIZ
@bot.message_handler(commands=['q'])
def quiz(msg):

    perguntas=[
    "Qual linguagem este bot usa?\nPython ou Java?",
    "Você gosta da KaoriBot?\nSim ou Sim?"
    ]

    bot.send_message(msg.chat.id,random.choice(perguntas))

# PIN
@bot.message_handler(commands=['pin'])
def pin(msg):

    if msg.reply_to_message:

        bot.pin_chat_message(
        msg.chat.id,
        msg.reply_to_message.message_id)

        bot.send_message(msg.chat.id,"Mensagem fixada")

# UNPIN
@bot.message_handler(commands=['unpin'])
def unpin(msg):

    bot.unpin_chat_message(msg.chat.id)
    bot.send_message(msg.chat.id,"Mensagens desafixadas")

# PING
@bot.message_handler(commands=['ping'])
def ping(msg):
    bot.send_message(msg.chat.id,"🏓 Pong!")

# UPTIME
@bot.message_handler(commands=['up'])
def uptime(msg):

    uptime=int(time.time()-start_time)

    h=uptime//3600
    m=(uptime%3600)//60
    s=uptime%60

    bot.send_message(msg.chat.id,
    f"Uptime:\n{h}h {m}m {s}s")

# STATS
@bot.message_handler(commands=['stats'])
def stats(msg):

    bot.send_message(msg.chat.id,
    "🌸 KaoriBot\nVersão 1.0")

# BOAS VINDAS
@bot.message_handler(content_types=['new_chat_members'])
def welcome(msg):

    for user in msg.new_chat_members:

        bot.send_message(
        msg.chat.id,
        f"🌸 Bem vindo {user.first_name}")

print("KaoriBot online")

bot.infinity_polling()