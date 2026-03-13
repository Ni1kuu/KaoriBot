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
        "/waifu+18 – Waifu +18 (somente privado)\n"
        "/gif – GIF de anime (safe)\n"
        "/gif+18 – GIF de anime +18 (somente privado)\n"
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
# /anagrama
# -----------------------------
@bot.message_handler(commands=['anagrama'])
def anagrama(message):
    chat_id = message.chat.id
    palavra = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(4,8)))
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
# /waifu e /waifu+18
# -----------------------------
@bot.message_handler(commands=['waifu','waifu+18'])
def waifu(message):
    cmd = message.text.split()[0]
    if cmd == 'waifu+18' and message.chat.type != 'private':
        bot.reply_to(message, "💛 Comando +18 só funciona em chat privado!")
        return
    tipo = 'nsfw' if cmd == 'waifu+18' else 'sfw'
    try:
        resp = requests.get(f"https://api.waifu.pics/{tipo}/waifu").json()
        bot.send_photo(message.chat.id, resp['url'])
    except:
        bot.reply_to(message, "💛 Não consegui pegar uma waifu agora 😢")

# -----------------------------
# /gif e /gif+18
# -----------------------------
@bot.message_handler(commands=['gif','gif+18'])
def anime_gif(message):
    cmd = message.text.split()[0]
    if cmd == 'gif+18' and message.chat.type != 'private':
        bot.reply_to(message, "💛 Comando +18 só funciona em chat privado!")
        return
    tipo = 'nsfw' if cmd == 'gif+18' else 'sfw'
    try:
        resp = requests.get(f"https://api.waifu.pics/{tipo}/hug").json()  # Pode usar hug/kiss aleatório
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
# /search
# -----------------------------
@bot.message_handler(commands=['search'])
def search(message):
    termo = message.text.replace('/search','').strip()
    if termo == "":
        bot.reply_to(message, "💛 Use: /search [termo]")
        return
    try:
        url = f"https://www.google.com/search?tbm=isch&q={termo.replace(' ','+')}"
        bot.send_message(message.chat.id, f"💛 Pesquisa: {url}")
    except:
        bot.reply_to(message, "💛 Não consegui fazer a pesquisa 😢")

# -----------------------------
# /antilink ON/OFF
# -----------------------------
@bot.message_handler(commands=['antilink'])
def toggle_antilink(message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) == 2 and args[1] in ['1','0']:
        antilink_ativo[chat_id] = args[1]=='1'
        status = 'ativado' if args[1]=='1' else 'desativado'
        bot.reply_to(message, f"💛 Antilink {status} neste grupo!")
    else:
        bot.reply_to(message, "💛 Use: /antilink 1 para ativar, /antilink 0 para desativar")

# -----------------------------
# Verificar links com ban
# -----------------------------
@bot.message_handler(func=lambda m: True)
def verificar_links(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    texto = message.text or ""
    if antilink_ativo.get(chat_id, False):
        if 'http://' in texto.lower() or 'https://' in texto.lower() or 'www.' in texto.lower():
            try:
                bot.delete_message(chat_id, message.message_id)
                bot.ban_chat_member(chat_id, user_id)
                bot.send_message(chat_id, f"💛 @{message.from_user.username} foi banido por enviar link!")
            except:
                bot.send_message(chat_id, "💛 Não consigo banir este usuário. Verifique as permissões do bot.")

# -----------------------------
# /ban manual
# -----------------------------
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not message.reply_to_message and len(message.text.split()) < 2:
        bot.reply_to(message, "💛 Use /ban @usuário ou responda a mensagem do usuário que deseja banir")
        return
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            username = message.text.split()[1].replace("@","")
            user_id = bot.get_chat_member(message.chat.id, username).user.id
        bot.ban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, f"💛 Usuário banido com sucesso!")
    except:
        bot.reply_to(message, "💛 Não foi possível banir o usuário. Verifique permissões ou nome correto.")

# -----------------------------
# Inicia o bot
# -----------------------------
bot.infinity_polling()