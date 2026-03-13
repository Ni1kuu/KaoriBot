import os
import random
import telebot
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# -----------------------------
# Variáveis globais
# -----------------------------
jogos_ativos = {}       # Para /anagrama
antilink_ativo = {}     # Para /antilink

# -----------------------------
# Lista gigante de palavras para /anagrama
# -----------------------------
palavras = [
    "banana","computador","gato","flor","jogo","anime","programa",
    "livro","carro","telefone","universo","planeta","python","internet",
    "amizade","escola","futebol","caneta","cadeira","musica","montanha",
    "cachorro","passaro","praia","cidade","filme","historia","familia",
    "trabalho","notebook","chuva","sol","lua","estrela","amizade","sonho",
    # ...adicione mais palavras para aumentar infinitamente
]

# -----------------------------
# Menu completo
# -----------------------------
@bot.message_handler(commands=['start','menu'])
def start_menu(message):
    menu_text = (
        "🌻💛 MENU KAORI 🌻💛\n"
        "╭━━━━━━━━━━━━━━━━━━━━╮\n"
        "💛 ⚙️ SISTEMA:\n"
        "/start – Iniciar o bot\n"
        "/ping – Testar tempo de resposta\n"
        "/menu – Ver este menu\n"
        "/anagrama – Jogo de palavras embaralhadas\n\n"
        "💛 📌 FIXAR MENSAGENS:\n"
        "/pin – Fixar a última mensagem do chat\n"
        "/unpin – Desafixar mensagens fixadas (resposta ou todas)\n\n"
        "💛 🌸 DIVERSÃO:\n"
        "/waifu – Puxar waifu aleatória (safe)\n"
        "/waifunsfw – Waifu +18 (somente privado)\n"
        "/gif – GIF de anime (safe)\n"
        "/gifnsfw – GIF de anime +18 (somente privado)\n"
        "/hug – Abraço anime (safe)\n"
        "/kiss – Beijo anime (safe)\n"
        "/meme – Meme aleatório em português\n"
        "/neko – Gato anime aleatório\n"
        "/8ball – Bola 8 mágica\n"
        "/roll – Rolar dado 🎲\n"
        "/quote – Frase motivacional 🌻\n"
        "/coin – Cara ou coroa 🪙\n\n"
        "💛 🛠 SISTEMA AVANÇADO:\n"
        "/userinfo – Info do usuário\n"
        "/chatinfo – Info do chat\n"
        "/say – O bot repete o que você digitar\n"
        "/avatar – Mostra sua foto de perfil\n"
        "/clear – Limpar últimas N mensagens (bot e admin)\n"
        "/clearall – Apagar mensagens (bot ou grupo)\n"
        "/search – Pesquisa no Google e retorna link\n"
        "/antilink 1/0 – Ativa/Desativa antilink com ban\n"
        "/ban – Banir usuário manualmente\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )
    bot.send_message(message.chat.id, menu_text)

# -----------------------------
# /ping
# -----------------------------
@bot.message_handler(commands=['ping'])
def ping(message):
    import time
    start = time.time()
    msg = bot.send_message(message.chat.id, "💛 Pingando...")
    end = time.time()
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                          text=f"🏓 Pong! Latência: {round((end-start)*1000)}ms")

# -----------------------------
# /anagrama
# -----------------------------
@bot.message_handler(commands=['anagrama'])
def anagrama(message):
    chat_id = message.chat.id
    palavra = random.choice(palavras)
    embaralhada = ''.join(random.sample(palavra, len(palavra)))
    jogos_ativos[chat_id] = palavra
    bot.send_message(chat_id, f"💛 Adivinhe a palavra: {embaralhada}")

@bot.message_handler(func=lambda m: m.chat.id in jogos_ativos)
def verificar_resposta(message):
    chat_id = message.chat.id
    palavra_correta = jogos_ativos.get(chat_id)
    if message.text.lower() == palavra_correta.lower():
        bot.reply_to(message, f"🌻 @{message.from_user.username} acertou, parabéns! 💛")
        jogos_ativos.pop(chat_id)

# -----------------------------
# /waifu e /waifunsfw
# -----------------------------
@bot.message_handler(commands=['waifu','waifunsfw'])
def waifu(message):
    cmd = message.text.split()[0]
    if cmd == 'waifunsfw' and message.chat.type != 'private':
        bot.reply_to(message, "💛 Comando NSFW só funciona em chat privado!")
        return
    tipo = 'nsfw' if cmd == 'waifunsfw' else 'sfw'
    try:
        resp = requests.get(f"https://api.waifu.pics/{tipo}/waifu").json()
        bot.send_photo(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, "💛 Não consegui pegar uma waifu agora 😢")

# -----------------------------
# /gif e /gifnsfw
# -----------------------------
@bot.message_handler(commands=['gif','gifnsfw'])
def anime_gif(message):
    cmd = message.text.split()[0]
    if cmd == 'gifnsfw' and message.chat.type != 'private':
        bot.reply_to(message, "💛 Comando NSFW só funciona em chat privado!")
        return
    tipo = 'nsfw' if cmd == 'gifnsfw' else 'sfw'
    try:
        resp = requests.get(f"https://api.waifu.pics/{tipo}/hug").json()  # hug aleatório
        bot.send_animation(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, f"💛 Não consegui enviar {cmd} agora 😢")

# -----------------------------
# /hug e /kiss (safe)
# -----------------------------
@bot.message_handler(commands=['hug','kiss'])
def hug_kiss(message):
    cmd = message.text.split()[0]
    tipo = 'sfw'
    try:
        resp = requests.get(f"https://api.waifu.pics/{tipo}/{cmd}").json()
        bot.send_animation(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, f"💛 Não consegui enviar {cmd} agora 😢")

# -----------------------------
# /meme
# -----------------------------
@bot.message_handler(commands=['meme'])
def meme(message):
    try:
        resp = requests.get("https://meme-api.com/gimme/ptmemes").json()
        bot.send_photo(message.chat.id, resp['url'], caption=resp['title'])
    except:
        bot.reply_to(message, "💛 Não consegui pegar um meme agora 😢")

# -----------------------------
# /neko
# -----------------------------
@bot.message_handler(commands=['neko'])
def neko(message):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/neko").json()
        bot.send_photo(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, "💛 Não consegui pegar um neko agora 😢")

# -----------------------------
# /8ball
# -----------------------------
respostas_8ball = [
    "Sim","Não","Talvez","Com certeza","Não sei","Pergunte mais tarde"
]
@bot.message_handler(commands=['8ball'])
def bola8(message):
    resp = random.choice(respostas_8ball)
    bot.send_message(message.chat.id, f"🎱 {resp}")

# -----------------------------
# /roll
# -----------------------------
@bot.message_handler(commands=['roll'])
def roll(message):
    bot.send_message(message.chat.id, f"🎲 Você tirou: {random.randint(1,6)}")

# -----------------------------
# /quote
# -----------------------------
frases = ["Acredite em você","Nunca desista","Hoje é um novo dia","Seja gentil","Siga seus sonhos"]
@bot.message_handler(commands=['quote'])
def quote(message):
    bot.send_message(message.chat.id, f"🌻 {random.choice(frases)}")

# -----------------------------
# /coin
# -----------------------------
@bot.message_handler(commands=['coin'])
def coin(message):
    bot.send_message(message.chat.id, f"🪙 {random.choice(['Cara','Coroa'])}")

# -----------------------------
# /userinfo
# -----------------------------
@bot.message_handler(commands=['userinfo'])
def userinfo(message):
    user = message.from_user
    bot.send_message(message.chat.id,
                     f"💛 Usuário: @{user.username}\nID: {user.id}\nNome: {user.first_name}")

# -----------------------------
# /chatinfo
# -----------------------------
@bot.message_handler(commands=['chatinfo'])
def chatinfo(message):
    chat = message.chat
    bot.send_message(chat.id,
                     f"💛 Chat: {chat.title}\nID: {chat.id}\nTipo: {chat.type}")

# -----------------------------
# /say
# -----------------------------
@bot.message_handler(commands=['say'])
def say(message):
    texto = message.text.replace('/say','').strip()
    if texto:
        bot.send_message(message.chat.id, texto)

# -----------------------------
# /avatar
# -----------------------------
@bot.message_handler(commands=['avatar'])
def avatar(message):
    user = message.from_user
    photos = bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        file_id = photos.photos[0][0].file_id
        bot.send_photo(message.chat.id, file_id)
    else:
        bot.send_message(message.chat.id, "💛 Sem foto de perfil.")

# -----------------------------
# /clear
# -----------------------------
@bot.message_handler(commands=['clear'])
def clear(message):
    args = message.text.split()
    if len(args)<2 or not args[1].isdigit():
        bot.reply_to(message,"💛 Use: /clear [número de mensagens]")
        return
    n = int(args[1])
    chat_id = message.chat.id
    msgs = bot.get_chat_history(chat_id, limit=n+1)
    for m in msgs:
        try: bot.delete_message(chat_id, m.message_id)
        except: pass

# -----------------------------
# /clearall
# -----------------------------
@bot.message_handler(commands=['clearall'])
def clearall(message):
    chat_id = message.chat.id
    msgs = bot.get_chat_history(chat_id, limit=100)  # Últimas 100 mensagens
    for m in msgs:
        try: bot.delete_message(chat_id, m.message_id)
        except: pass

# -----------------------------
# /search
# -----------------------------
@bot.message_handler(commands=['search'])
def search(message):
    termo = message.text.replace('/search','').strip()
    if termo == "":
        bot.reply_to(message, "💛 Use: /search [termo]")
        return
    url = f"https://www.google.com/search?q={termo.replace(' ','+')}"
    bot.send_message(message.chat.id, f"💛 Pesquisa: {url}")

# -----------------------------
# /antilink
# -----------------------------
@bot.message_handler(commands=['antilink'])
def toggle_antilink(message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args)==2 and args[1] in ['1','0']:
        antilink_ativo[chat_id] = args[1]=='1'
        bot.reply_to(message, f"💛 Antilink {'ativado' if args[1]=='1' else 'desativado'}")
    else:
        bot.reply_to(message, "💛 Use /antilink 1 para ativar, /antilink 0 para desativar")

@bot.message_handler(func=lambda m: True)
def verificar_links(message):
    chat_id = message.chat.id
    if antilink_ativo.get(chat_id, False):
        texto = message.text.lower() if message.text else ""
        if any(x in texto for x in ['http://','https://','www.']):
            try:
                bot.delete_message(chat_id, message.message_id)
                bot.ban_chat_member(chat_id, message.from_user.id)
                bot.send_message(chat_id, f"💛 @{message.from_user.username} foi banido por enviar link!")
            except: pass

# -----------------------------
# /ban manual
# -----------------------------
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            bot.ban_chat_member(message.chat.id, user_id)
            bot.reply_to(message, f"💛 Usuário banido com sucesso!")
        except:
            bot.reply_to(message, "💛 Não foi possível banir este usuário.")
    else:
        bot.reply_to(message,"💛 Responda a mensagem do usuário que deseja banir.")

# -----------------------------
# /pin e /unpin
# -----------------------------
@bot.message_handler(commands=['pin'])
def pin(message):
    try:
        bot.pin_chat_message(message.chat.id, message.message_id-1)
        bot.reply_to(message,"💛 Mensagem fixada!")
    except:
        bot.reply_to(message,"💛 Não foi possível fixar a mensagem.")

@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message,"💛 Todas mensagens desafixadas!")
    except:
        bot.reply_to(message,"💛 Não foi possível desafixar mensagens.")

# -----------------------------
# Inicia o bot
# -----------------------------
bot.infinity_polling()