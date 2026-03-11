import os
import random
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

MENU = """
╭━━━🌸 MENU KAORI 🌸━━━╮

/start → iniciar bot
/menu → abrir menu
/ping → verificar bot
/numero → número aleatório
/repetir → repetir mensagem
/fig → criar figurinha

"""

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.effective_user.first_name

    await update.message.reply_text(
        f"Oii {nome}! 🌸\nEu sou a Kaori ꒰ᐢ. .ᐢ꒱\nUse /menu para ver meus comandos!"
    )

# MENU
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(MENU)

# PING
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Pong! Estou online 🌸"
    )

# NÚMERO
async def numero(update: Update, context: ContextTypes.DEFAULT_TYPE):

    n = random.randint(1,100)

    await update.message.reply_text(
        f"🎲 Seu número é {n}! Espero que seja sorte ꒰ᐢ. .ᐢ꒱"
    )

# REPETIR
async def repetir(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Use assim:\n/repetir mensagem"
        )
        return

    texto = " ".join(context.args)

    await update.message.reply_text(
        f"{texto} 🌸"
    )

# FIGURINHA
async def fig(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Responda uma imagem com /fig 🌸"
        )
        return

    msg = update.message.reply_to_message

    if not msg.photo:
        await update.message.reply_text(
            "Isso não parece uma imagem 😿"
        )
        return

    photo = msg.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    await file.download_to_drive("img.png")

    img = Image.open("img.png")

    img = img.resize((512,512))

    img.save("sticker.webp","WEBP")

    with open("sticker.webp","rb") as s:

        await update.message.reply_sticker(s)

# MAIN
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("numero", numero))
    app.add_handler(CommandHandler("repetir", repetir))
    app.add_handler(CommandHandler("fig", fig))

    print("🌸 Kaori V1 online!")

    app.run_polling()

main()