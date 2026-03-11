import random
import time
import os
from PIL import Image
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
OWNER = int(os.getenv("7659474646", "0"))

start_time = time.time()

bot_ativo = True
anti_link = False
bem_vindo = False

# ======================
# MENU
# ======================

MENU = """
╭━━━🌸 MENU KAORI BOT 🌸━━━╮

👤 Usuário
/start (/s)
/id
/perfil
/avatar
/menu
/info
/dica
/prefixo
/fig

🎮 Diversão
/numero (/n)
/repetir (/rm)
/resposta (/r)
/forca (/f)
/caraoucoroa (/c)
/rolardado (/ro)
/piada (/p)
/quiz (/q)

🛡 Moderação
/pin
/unpin
/ban
/kick
/mute
/unmute
/ativarbemvindo
/desativarbemvindo
/ativarlinks
/desativarlinks

🤖 Bot
/ping
/up
/status
/on
/off
"""

# ======================
# USUÁRIO
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Oii {update.effective_user.first_name}! 🌸\nEu sou a Kaori ꒰ᐢ. .ᐢ꒱₊˚⊹\nUse /menu para ver meus comandos!"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU)

async def id_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Seu ID é `{update.effective_user.id}` 🌸"
    )

async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    txt = f"""
🌸 Perfil

Nome: {u.first_name}
ID: {u.id}

Kaori acha você incrível ꒰ᐢ. .ᐢ꒱
"""
    await update.message.reply_text(txt)

async def avatar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = await context.bot.get_user_profile_photos(update.effective_user.id)

    if photos.total_count == 0:
        await update.message.reply_text("Você não tem avatar 😿")
        return

    await update.message.reply_photo(photos.photos[0][-1].file_id)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Eu sou a Kaori 🌸\nUm bot fofinho feito para ajudar!"
    )

async def dica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Dica da Kaori 🌸\nResponda uma imagem com /fig para criar uma figurinha!"
    )

async def prefixo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Prefixo principal: /\nExemplo: /start ou /s"
    )

# ======================
# FIGURINHA
# ======================

async def fig(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Responda uma imagem com /fig 🌸")
        return

    msg = update.message.reply_to_message

    if not msg.photo:
        await update.message.reply_text("Isso não é uma imagem 😿")
        return

    photo = msg.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    await file.download_to_drive("img.png")

    img = Image.open("img.png")

    img = img.resize((512,512))

    img.save("sticker.webp","WEBP")

    with open("sticker.webp","rb") as s:
        await update.message.reply_sticker(s)

    os.remove("img.png")
    os.remove("sticker.webp")

# ======================
# DIVERSÃO
# ======================

async def numero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    n = random.randint(1,100)
    await update.message.reply_text(
        f"🎲 Seu número é {n}! Boa sorte ꒰ᐢ. .ᐢ꒱"
    )

async def repetir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /repetir mensagem")
        return

    texto = " ".join(context.args)

    await update.message.reply_text(f"{texto} 🌸")

async def resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    respostas = [
        "Sim! 🌸",
        "Talvez 🤭",
        "Não 😿",
        "Com certeza!",
        "Hmm... acho que sim ꒰ᐢ. .ᐢ꒱"
    ]

    await update.message.reply_text(random.choice(respostas))

async def cara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(["Cara 🪙","Coroa 🪙"]))

async def dado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎲 Resultado: {random.randint(1,20)}"
    )

async def piada(update: Update, context: ContextTypes.DEFAULT_TYPE):

    piadas = [
        "Por que o computador foi ao médico? Porque estava com vírus 🤭",
        "Qual café é mais perigoso? O ex-presso ☕",
        "O que o zero disse pro oito? Belo cinto!"
    ]

    await update.message.reply_text(random.choice(piadas))

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Quiz da Kaori 🌸\nQual a capital do Brasil?\nA) Rio\nB) Brasília\nC) SP"
    )

async def forca(update: Update, context: ContextTypes.DEFAULT_TYPE):

    palavras = ["gato","anime","flor","telegram"]

    p = random.choice(palavras)

    await update.message.reply_text(
        f"Forca! A palavra tem {len(p)} letras ꒰ᐢ. .ᐢ꒱"
    )

# ======================
# MODERAÇÃO
# ======================

async def ativarlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link
    anti_link = True
    await update.message.reply_text("🚫 Anti-link ativado! Kaori vai proteger o grupo 🌸")

async def desativarlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link
    anti_link = False
    await update.message.reply_text("Anti-link desativado 🌸")

async def detectar_links(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global anti_link

    if not anti_link:
        return

    if not update.message.text:
        return

    texto = update.message.text.lower()

    links = ["http","https","t.me","www"]

    if any(link in texto for link in links):

        user = update.message.from_user.id
        chat = update.effective_chat.id

        try:
            await update.message.delete()

            await context.bot.ban_chat_member(chat, user)

            await context.bot.send_message(
                chat,
                "🚫 Link proibido!\nUsuário removido pela Kaori 🌸"
            )

        except:
            pass

# ======================
# STATUS
# ======================

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! Estou online 🌸")

async def up(update: Update, context: ContextTypes.DEFAULT_TYPE):

    tempo = int(time.time() - start_time)

    await update.message.reply_text(
        f"Estou online há {tempo} segundos ⏱"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Tudo funcionando perfeitamente! ✨"
    )

async def on(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER:
        return

    global bot_ativo

    bot_ativo = True

    await update.message.reply_text("Bot ativado 🌸")

async def off(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER:
        return

    global bot_ativo

    bot_ativo = False

    await update.message.reply_text("Bot desativado 😴")

# ======================
# MAIN
# ======================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler(["start","s"], start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("id", id_user))
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("avatar", avatar))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("dica", dica))
    app.add_handler(CommandHandler("prefixo", prefixo))

    app.add_handler(CommandHandler("fig", fig))

    app.add_handler(CommandHandler(["numero","n"], numero))
    app.add_handler(CommandHandler(["repetir","rm"], repetir))
    app.add_handler(CommandHandler(["resposta","r"], resposta))
    app.add_handler(CommandHandler(["forca","f"], forca))
    app.add_handler(CommandHandler(["caraoucoroa","c"], cara))
    app.add_handler(CommandHandler(["rolardado","ro"], dado))
    app.add_handler(CommandHandler(["piada","p"], piada))
    app.add_handler(CommandHandler(["quiz","q"], quiz))

    app.add_handler(CommandHandler("ativarlinks", ativarlinks))
    app.add_handler(CommandHandler("desativarlinks", desativarlinks))

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("up", up))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("on", on))
    app.add_handler(CommandHandler("off", off))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detectar_links))

    print("🌸 Kaori online!")

    app.run_polling()

main()