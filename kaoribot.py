import os
import time
import requests
import wikipedia
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
GIPHY = os.getenv("GIPHY_KEY")

inicio = time.time()

def uptime():
    u = int(time.time() - inicio)
    h = u // 3600
    m = (u % 3600) // 60
    s = u % 60
    return f"{h}h {m}m {s}s"


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌻 Olá! Eu sou a Kaori!\nUse /menu para ver meus comandos."
    )


# MENU
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
🌻 COMANDOS KAORI 🌻

╭━━👤 Usuário━━╮
/start → Iniciar
/info → Informações
/whoami → Quem sou eu
/avatar → Ver avatar

╭━━⚡ Sistema━━╮
/ping → Ping do bot
/clear → Limpar mensagens
/pin → Fixar mensagem
/unpin → Desafixar mensagem

╭━━🔎 Pesquisa━━╮
/google → Pesquisa Google
/img → Buscar imagem
/gif → Buscar gif
/wiki → Buscar Wikipedia
/wikiing → Resumo Wiki
/traduza → Traduzir texto
/shortlink → Encurtar link

╰━━━━━━━━━━━━━━━━━━━━╯
"""

    await update.message.reply_text(texto)


# INFO
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"""🌻 KAORI BOT 🌻

Criador: Nikuu 
Versão: 1.0
Criação: 09/03/2026
Uptime: {uptime()}
"""
    )


# WHOAMI
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await update.message.reply_text(
        f"""👤 Seu Perfil

Nome: {user.first_name}
ID: {user.id}
Username: @{user.username}
"""
    )


# AVATAR
async def avatar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    fotos = await context.bot.get_user_profile_photos(user.id)

    if fotos.total_count > 0:
        await update.message.reply_photo(
            fotos.photos[0][-1].file_id
        )
    else:
        await update.message.reply_text("Usuário não tem avatar.")


# PING
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    inicio_ping = time.time()

    msg = await update.message.reply_text("🏓 Pong...")

    fim = time.time()

    ms = int((fim - inicio_ping) * 1000)

    await msg.edit_text(f"🏓 Pong: {ms}ms")


# CLEAR
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        for i in range(1, 50):
            await context.bot.delete_message(
                update.effective_chat.id,
                update.message.message_id - i
            )
    except:
        pass


# PIN
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.reply_to_message:

        await context.bot.pin_chat_message(
            update.effective_chat.id,
            update.message.reply_to_message.message_id
        )

    else:
        await update.message.reply_text(
            "Responda a mensagem que deseja fixar."
        )


# UNPIN
async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.unpin_chat_message(update.effective_chat.id)


# GOOGLE
async def google(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /google algo")
        return

    query = " ".join(context.args)

    link = f"https://www.google.com/search?q={query}"

    await update.message.reply_text(link)


# IMG
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /img algo")
        return

    query = " ".join(context.args)

    url = f"https://source.unsplash.com/600x400/?{query}"

    await update.message.reply_photo(url)


# GIF
async def gif(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /gif algo")
        return

    query = " ".join(context.args)

    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY}&q={query}&limit=1"

    data = requests.get(url).json()

    try:
        gif_url = data["data"][0]["images"]["original"]["url"]

        await update.message.reply_animation(gif_url)

    except:
        await update.message.reply_text("Gif não encontrado.")


# WIKI LINK
async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wikipedia.set_lang("pt")

    query = " ".join(context.args)

    try:

        page = wikipedia.page(query)

        await update.message.reply_text(page.url)

    except:

        await update.message.reply_text("Não encontrei isso.")


# WIKI RESUMO
async def wikiing(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wikipedia.set_lang("pt")

    query = " ".join(context.args)

    try:

        resumo = wikipedia.summary(query, sentences=3)

        await update.message.reply_text(resumo)

    except:

        await update.message.reply_text("Não encontrei isso.")


# TRADUZIR
async def traduza(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = " ".join(context.args)

    url = f"https://api.mymemory.translated.net/get?q={texto}&langpair=auto|pt"

    r = requests.get(url).json()

    traducao = r["responseData"]["translatedText"]

    await update.message.reply_text(traducao)


# SHORTLINK
async def shortlink(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /shortlink link")
        return

    link = context.args[0]

    api = f"https://tinyurl.com/api-create.php?url={link}"

    short = requests.get(api).text

    await update.message.reply_text(short)


# BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("whoami", whoami))
app.add_handler(CommandHandler("avatar", avatar))

app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(CommandHandler("pin", pin))
app.add_handler(CommandHandler("unpin", unpin))

app.add_handler(CommandHandler("google", google))
app.add_handler(CommandHandler("img", img))
app.add_handler(CommandHandler("gif", gif))
app.add_handler(CommandHandler("wiki", wiki))
app.add_handler(CommandHandler("wikiing", wikiing))
app.add_handler(CommandHandler("traduza", traduza))
app.add_handler(CommandHandler("shortlink", shortlink))

print("🌻 Kaori está online!")

app.run_polling()