import os
import telebot
import requests
import random
import time

# -------------------------
# VARIÁVEIS
TOKEN = os.getenv("BOT_TOKEN")  # Coloque no Railway Secrets
GIPHY_KEY = os.getenv("GIPHY_KEY")  # Coloque sua Giphy API Key no Railway
bot = telebot.TeleBot(TOKEN)

# -------------------------
# COMANDOS PRINCIPAIS

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "💛 Olá! Eu sou a KaoriBot 💛\nUse /menu para ver todos os comandos.")

# /ping - tempo de resposta em segundos
@bot.message_handler(commands=['ping'])
def ping(message):
    start = time.time()
    msg = bot.send_message(message.chat.id, "🏓 Pingando... 💛🌻")
    end = time.time()
    tempo = end - start
    bot.edit_message_text(f"🏓 Pong! Tempo de resposta: {tempo:.3f} segundos 💛🌻", 
                          message.chat.id, msg.message_id)

# /menu - menu estilizado atualizado
@bot.message_handler(commands=['menu'])
def menu(message):
    menu_text = (
        "╭━━ 💛🌻 MENU KAORI 🌻💛 ━━╮\n\n"
        "💛 ⚙️ SISTEMA:\n"
        "💛 /start – Iniciar o bot\n"
        "💛 /ping – Testar tempo de resposta\n"
        "💛 /menu – Ver este menu\n\n"
        "💛 📌 FIXAR MENSAGENS:\n"
        "💛 /pin – Fixar a última mensagem do chat\n"
        "💛 /unpin – Desafixar mensagens fixadas (resposta ou todas)\n\n"
        "💛 🌸 DIVERSÃO:\n"
        "💛 /waifu – Puxar waifu aleatória\n"
        "💛 /hug – Enviar abraço em GIF (Giphy)\n"
        "💛 /kiss – Enviar beijo em GIF (Giphy)\n"
        "💛 /meme – Puxar meme aleatório em português\n"
        "💛 /neko – Puxar gato anime aleatório\n"
        "💛 /8ball – Bola 8 mágica\n"
        "💛 /roll – Rolar dado 🎲\n"
        "💛 /quote – Frase motivacional 🌻\n"
        "💛 /coin – Cara ou coroa 🪙\n\n"
        "💛 🛠 SISTEMA AVANÇADO:\n"
        "💛 /userinfo – Info do usuário\n"
        "💛 /chatinfo – Info do chat\n"
        "💛 /say – O bot repete o que você digitar\n"
        "💛 /avatar – Mostra sua foto de perfil\n"
        "💛 /clear – Limpar últimas N mensagens (bot e admin)\n"
        "💛 /clearall – Apagar mensagens (bot ou grupo, dependendo do chat)\n"
        "💛 /search – Pesquisa no Google e retorna link\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )
    bot.reply_to(message, menu_text)

# -------------------------
# PIN / UNPIN

@bot.message_handler(commands=['pin'])
def pin(message):
    try:
        bot.pin_chat_message(message.chat.id, message.message_id)
        bot.reply_to(message, "💛 Mensagem fixada com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao fixar: {e}")

# /unpin inteligente
@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        # Se estiver respondendo a uma mensagem, desfixa apenas ela
        if message.reply_to_message:
            bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
            bot.reply_to(message, "💛 Mensagem desfixada com sucesso!")
        else:
            # Caso contrário, desfixa todas
            bot.unpin_all_chat_messages(message.chat.id)
            bot.reply_to(message, "💛 Todas as mensagens fixadas foram desafixadas!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao desafixar: {e}")

# -------------------------
# COMANDOS DE DIVERSÃO

# /waifu
@bot.message_handler(commands=['waifu'])
def waifu(message):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/waifu").json()
        bot.send_photo(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, "💛 Não consegui buscar a waifu 😢")

# /hug - GIF aleatório Giphy
@bot.message_handler(commands=['hug'])
def hug(message):
    try:
        url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_KEY}&tag=hug&rating=pg-13"
        resp = requests.get(url).json()
        gif_url = resp['data']['images']['original']['url']
        bot.send_animation(message.chat.id, gif_url)
    except:
        bot.reply_to(message, "💛 Não consegui buscar um hug 😢")

# /kiss - GIF aleatório Giphy
@bot.message_handler(commands=['kiss'])
def kiss(message):
    try:
        url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_KEY}&tag=kiss&rating=pg-13"
        resp = requests.get(url).json()
        gif_url = resp['data']['images']['original']['url']
        bot.send_animation(message.chat.id, gif_url)
    except:
        bot.reply_to(message, "💛 Não consegui buscar um kiss 😢")

# /meme
@bot.message_handler(commands=['meme'])
def meme(message):
    try:
        resp = requests.get("https://meme-api.com/gimme/ptbr").json()
        bot.send_photo(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, "💛 Não consegui pegar um meme 😢")

# /neko
@bot.message_handler(commands=['neko'])
def neko(message):
    try:
        resp = requests.get("https://api.waifu.pics/sfw/neko").json()
        bot.send_photo(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, "💛 Não consegui pegar o neko 😢")

# /8ball
@bot.message_handler(commands=['8ball'])
def eight_ball(message):
    respostas = ["Sim 💛", "Não 😢", "Talvez… 🌻", "Com certeza! 💛", 
                 "Não conte com isso 😅", "Provavelmente 💛", "Impossível 😭"]
    bot.reply_to(message, random.choice(respostas))

# /roll
@bot.message_handler(commands=['roll'])
def roll(message):
    numero = random.randint(1, 6)
    bot.reply_to(message, f"🎲 Você tirou: {numero}")

# /quote
@bot.message_handler(commands=['quote'])
def quote(message):
    frases = [
        "💛 Acredite em você mesmo 🌻",
        "💛 Cada dia é uma nova chance 🌻",
        "💛 Nunca desista dos seus sonhos 🌻",
        "💛 Pequenos passos também levam longe 🌻",
        "💛 Seja gentil, sempre 🌻"
    ]
    bot.reply_to(message, random.choice(frases))

# /coin
@bot.message_handler(commands=['coin'])
def coin(message):
    lado = random.choice(["Cara 💛", "Coroa 🌻"])
    bot.reply_to(message, f"🪙 O resultado é: {lado}")

# -------------------------
# COMANDOS DE SISTEMA/UTILIDADE

# /userinfo
@bot.message_handler(commands=['userinfo'])
def userinfo(message):
    user = message.from_user
    text = (
        f"💛 Nome: {user.first_name}\n"
        f"💛 Username: @{user.username if user.username else 'Sem username'}\n"
        f"💛 ID: {user.id}\n"
        f"💛 Bot: {user.is_bot}"
    )
    bot.reply_to(message, text)

# /chatinfo
@bot.message_handler(commands=['chatinfo'])
def chatinfo(message):
    chat = message.chat
    text = (
        f"💛 Nome do chat: {chat.title if chat.title else 'Chat privado'}\n"
        f"💛 ID do chat: {chat.id}\n"
        f"💛 Tipo: {chat.type}\n"
        f"💛 Members não disponíveis via bot API"
    )
    bot.reply_to(message, text)

# /say
@bot.message_handler(commands=['say'])
def say(message):
    text = message.text.replace('/say','').strip()
    if text:
        bot.send_message(message.chat.id, text)
    else:
        bot.reply_to(message, "💛 Digite algo para eu repetir!")

# /avatar
@bot.message_handler(commands=['avatar'])
def avatar(message):
    try:
        photos = bot.get_user_profile_photos(message.from_user.id)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            bot.send_photo(message.chat.id, file_id)
        else:
            bot.reply_to(message, "💛 Você não tem foto de perfil!")
    except Exception as e:
        bot.reply_to(message, f"💛 Erro ao buscar avatar: {e}")

# /clear - apagar últimas N mensagens possíveis
@bot.message_handler(commands=['clear'])
def clear(message):
    try:
        quantidade = int(message.text.replace('/clear','').strip())
        deleted = 0
        for msg_id in range(message.message_id-quantidade, message.message_id):
            try:
                bot.delete_message(message.chat.id, msg_id)
                deleted += 1
            except:
                pass
        bot.reply_to(message, f"💛 Tentei apagar {quantidade} mensagens. Apaguei {deleted}.")
    except:
        bot.reply_to(message, "💛 Use: /clear [quantidade de mensagens]")

# /clearall - apaga mensagens em chat privado ou grupo
@bot.message_handler(commands=['clearall'])
def clear_all(message):
    deleted = 0
    if message.chat.type in ["group","supergroup"]:
        for msg_id in range(message.message_id - 200, message.message_id):
            try:
                bot.delete_message(message.chat.id, msg_id)
                deleted += 1
            except:
                pass
        bot.reply_to(message, f"💛 Tentei apagar 200 mensagens. Apaguei {deleted}.")
    else:  # chat privado
        for msg_id in range(message.message_id - 50, message.message_id):
            try:
                bot.delete_message(message.chat.id, msg_id)
                deleted += 1
            except:
                pass
        bot.reply_to(message, f"💛 Tentei apagar 50 mensagens (somente minhas). Apaguei {deleted}.")

# /search - pesquisa no Google
@bot.message_handler(commands=['search'])
def search(message):
    termo = message.text.replace('/search','').strip()
    if termo:
        termo_formatado = termo.replace(' ', '+')
        link = f"https://www.google.com/search?q={termo_formatado}"
        bot.reply_to(message, f"💛 Resultado da pesquisa:\n{link}")
    else:
        bot.reply_to(message, "💛 Digite algo para pesquisar! Ex: /search gatos")

# -------------------------
# INICIAR BOT
print("KaoriBot online! 💛")
bot.infinity_polling()