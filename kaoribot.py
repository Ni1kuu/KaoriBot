import os
import random
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- ANAGRAMA LISTA ---
palavras_anagrama = ["amigo","banana","computador","desenvolvedor","python","telegram","kaoribot","mensagem","jogo","anime","gato","waifu","flor","coracao","sorriso"]

# --- /start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "💛 Olá! KaoriBot iniciada 🌻 Use /menu para ver os comandos.")

# --- /menu ---
@bot.message_handler(commands=['menu'])
def menu(message):
    texto_menu = """
╭━━ 💛🌻 MENU KAORI 🌻💛 ━━╮

💛 ⚙️ SISTEMA:
💛 /start – Iniciar o bot
💛 /ping – Testar tempo de resposta
💛 /menu – Ver este menu

💛 📌 FIXAR MENSAGENS:
💛 /pin – Fixar a última mensagem do chat
💛 /unpin – Desafixar mensagens fixadas (resposta ou todas)

💛 🌸 DIVERSÃO:
💛 /waifu – Puxar waifu aleatória
💛 /hug – Enviar abraço em GIF (Giphy)
💛 /kiss – Enviar beijo em GIF (Giphy)
💛 /meme – Puxar meme aleatório em português
💛 /neko – Puxar gato anime aleatório
💛 /8ball – Bola 8 mágica
💛 /roll – Rolar dado 🎲
💛 /quote – Frase motivacional 🌻
💛 /coin – Cara ou coroa 🪙

💛 🛠 SISTEMA AVANÇADO:
💛 /userinfo – Info do usuário
💛 /chatinfo – Info do chat
💛 /say – O bot repete o que você digitar
💛 /avatar – Mostra sua foto de perfil
💛 /clear – Limpar últimas N mensagens (bot e admin)
💛 /clearall – Apagar mensagens (bot ou grupo, dependendo do chat)
💛 /search – Pesquisa no Google e retorna link
💛 /antilink – Ativa/Desativa proteção de link
💛 /ban – Bane usuário
💛 /anagrama – Jogo de anagramas
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.reply_to(message, texto_menu)

# --- /ping ---
@bot.message_handler(commands=['ping'])
def ping(message):
    msg = bot.reply_to(message, "💛 Pingando...")
    bot.edit_message_text(f"🏓 Pong! Latência: {round(bot.get_me().id / 1000, 2)}s", message.chat.id, msg.message_id)

# --- /pin ---
@bot.message_handler(commands=['pin'])
def pin(message):
    try:
        bot.pin_chat_message(message.chat.id, message.message_id, disable_notification=True)
        bot.reply_to(message, "💛 Mensagem fixada com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"❌ Não foi possível fixar a mensagem.\nErro: {e}")

# --- /unpin ---
@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        if message.reply_to_message:
            bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
            bot.reply_to(message, "💛 Mensagem desfixada com sucesso!")
        else:
            bot.unpin_all_chat_messages(message.chat.id)
            bot.reply_to(message, "💛 Todas as mensagens fixadas foram desfixadas!")
    except Exception as e:
        bot.reply_to(message, f"❌ Não foi possível desfixar.\nErro: {e}")

# --- /waifu ---
@bot.message_handler(commands=['waifu'])
def waifu(message):
    resp = requests.get("https://api.waifu.pics/sfw/waifu").json()
    bot.send_photo(message.chat.id, resp['url'])

# --- /hug ---
@bot.message_handler(commands=['hug'])
def hug(message):
    resp = requests.get("https://api.waifu.pics/sfw/hug").json()
    bot.send_animation(message.chat.id, resp['url'])

# --- /kiss ---
@bot.message_handler(commands=['kiss'])
def kiss(message):
    resp = requests.get("https://api.waifu.pics/sfw/kiss").json()
    bot.send_animation(message.chat.id, resp['url'])

# --- /meme ---
@bot.message_handler(commands=['meme'])
def meme(message):
    resp = requests.get("https://meme-api.com/gimme/wholesomememes").json()
    bot.send_photo(message.chat.id, resp['url'])

# --- /neko ---
@bot.message_handler(commands=['neko'])
def neko(message):
    resp = requests.get("https://api.waifu.pics/sfw/neko").json()
    bot.send_photo(message.chat.id, resp['url'])

# --- /8ball ---
@bot.message_handler(commands=['8ball'])
def ball(message):
    respostas = ["Sim", "Não", "Talvez", "Claro!", "Duvido", "Com certeza", "Não conte com isso"]
    bot.reply_to(message, f"🎱 {random.choice(respostas)}")

# --- /roll ---
@bot.message_handler(commands=['roll'])
def roll(message):
    bot.reply_to(message, f"🎲 Você rolou: {random.randint(1,6)}")

# --- /quote ---
@bot.message_handler(commands=['quote'])
def quote(message):
    frases = [
        "🌻 A vida é bela!",
        "💛 Nunca desista dos seus sonhos.",
        "🌸 Acredite em você.",
        "💛 Cada dia é uma nova oportunidade."
    ]
    bot.reply_to(message, random.choice(frases))

# --- /coin ---
@bot.message_handler(commands=['coin'])
def coin(message):
    bot.reply_to(message, f"🪙 {'Cara' if random.randint(0,1)==0 else 'Coroa'}")

# --- /userinfo ---
@bot.message_handler(commands=['userinfo'])
def userinfo(message):
    user = message.from_user
    texto = f"💛 Usuário: {user.first_name} {user.last_name if user.last_name else ''}\nID: {user.id}\nUsername: @{user.username if user.username else 'Sem username'}"
    bot.reply_to(message, texto)

# --- /chatinfo ---
@bot.message_handler(commands=['chatinfo'])
def chatinfo(message):
    chat = message.chat
    texto = f"💛 Chat: {chat.title if chat.title else 'Privado'}\nID: {chat.id}\nTipo: {chat.type}"
    bot.reply_to(message, texto)

# --- /say ---
@bot.message_handler(commands=['say'])
def say(message):
    text = message.text.split(' ',1)
    if len(text)==2:
        bot.send_message(message.chat.id, text[1])
    else:
        bot.reply_to(message, "💛 Use: /say <mensagem>")

# --- /avatar ---
@bot.message_handler(commands=['avatar'])
def avatar(message):
    photos = bot.get_user_profile_photos(message.from_user.id)
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        bot.send_photo(message.chat.id, file_id)
    else:
        bot.reply_to(message, "💛 Você não tem foto de perfil.")

# --- /clear ---
@bot.message_handler(commands=['clear'])
def clear(message):
    try:
        args = message.text.split(' ')
        n = int(args[1]) if len(args) > 1 else 5
        for i in range(n):
            bot.delete_message(message.chat.id, message.message_id-i)
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao limpar mensagens: {e}")

# --- /clearall ---
@bot.message_handler(commands=['clearall'])
def clearall(message):
    bot.send_message(message.chat.id, "💛 Comando de limpeza total executado (limite de API Telegram).")

# --- /search ---
@bot.message_handler(commands=['search'])
def search_cmd(message):
    termo = message.text.split(' ',1)
    if len(termo) < 2:
        bot.reply_to(message, "💛 Use: /search <termo>")
        return
    query = termo[1].replace(' ','+')
    bot.send_message(message.chat.id, f"https://www.google.com/search?q={query}")

# --- /antilink ---
antilink_status = {}
@bot.message_handler(commands=['antilink'])
def antilink(message):
    chat_id = message.chat.id
    if chat_id not in antilink_status:
        antilink_status[chat_id] = True
        bot.reply_to(message, "💛 Antilink ativado!")
    else:
        antilink_status[chat_id] = not antilink_status[chat_id]
        bot.reply_to(message, f"💛 Antilink {'ativado' if antilink_status[chat_id] else 'desativado'}!")

@bot.message_handler(func=lambda m: True)
def check_antilink(message):
    if antilink_status.get(message.chat.id, False):
        if "http" in message.text.lower():
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass

# --- /ban ---
@bot.message_handler(commands=['ban'])
def ban(message):
    if not message.reply_to_message:
        bot.reply_to(message, "💛 Responda a mensagem do usuário para banir.")
        return
    try:
        bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "💛 Usuário banido com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"❌ Não foi possível banir: {e}")

# --- /anagrama ---
@bot.message_handler(commands=['anagrama'])
def anagrama(message):
    palavra = random.choice(palavras_anagrama)
    embaralhada = ''.join(random.sample(palavra,len(palavra)))
    msg = bot.reply_to(message, f"💛 Adivinhe a palavra: {embaralhada}")

    @bot.message_handler(func=lambda m: m.text.lower() == palavra.lower())
    def acertou(resp_msg):
        if resp_msg.chat.id == message.chat.id:
            bot.reply_to(resp_msg, f"💛 {resp_msg.from_user.first_name} acertou, parabéns!")

# --- INICIAR BOT ---
print("💛 KaoriBot iniciado...")
bot.infinity_polling()