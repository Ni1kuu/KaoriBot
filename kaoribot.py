import telebot
import random
import json
from datetime import datetime, timedelta

TOKEN = "8791892359:AAHgDmGvBNBueRDm5vwdZmT9Hjj1_LGhaTI"
CREATOR_ID = 7659474646  # substitua pelo seu ID
bot = telebot.TeleBot(TOKEN)

# ===============================
# Status do bot e funcionalidades
# ===============================
welcome_active = True       # Boas-vindas automática
links_block_active = False  # Bloqueio de links automático

# ===============================
# Dados RPG e Usuários
# ===============================
try:
    with open("rpg_data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

def init_user(user_id):
    if str(user_id) not in data:
        data[str(user_id)] = {
            "xp": 0,
            "level": 0,
            "coins": 15000 if user_id == CREATOR_ID else 0,
            "last_daily": None,
            "inventory": [],
            "missao": None,
            "last_missao": None
        }

def save_data():
    with open("rpg_data.json", "w") as f:
        json.dump(data, f, indent=4)

def add_xp(user_id, amount):
    init_user(user_id)
    total_xp = amount
    if "amuleto" in data[str(user_id)]["inventory"]:
        total_xp += int(amount * 0.2)
    data[str(user_id)]["xp"] += total_xp
    while data[str(user_id)]["xp"] >= (data[str(user_id)]["level"] + 1) * 100:
        data[str(user_id)]["xp"] -= (data[str(user_id)]["level"] + 1) * 100
        data[str(user_id)]["level"] += 1
    save_data()

def add_coins(user_id, amount):
    init_user(user_id)
    total = amount
    if "moedinha" in data[str(user_id)]["inventory"]:
        total += int(amount * 0.2)
    data[str(user_id)]["coins"] += total
    save_data()

# ===============================
# Funções RPG / Economia
# ===============================
loja = {
    "espada": 100,
    "escudo": 80,
    "poção": 50,
    "amuleto": 200,
    "moedinha": 150
}

def daily(user_id):
    init_user(user_id)
    now = datetime.now()
    last = data[str(user_id)]["last_daily"]
    if last:
        last_dt = datetime.fromisoformat(last)
        if now - last_dt < timedelta(hours=24):
            return f"Você já pegou sua recompensa diária! Volte em {24 - (now - last_dt).seconds//3600}h."
    reward = random.randint(50, 150)
    add_coins(user_id, reward)
    data[str(user_id)]["last_daily"] = now.isoformat()
    save_data()
    return f"Você recebeu {reward} coins no /daily!"

def missao(user_id):
    init_user(user_id)
    now = datetime.now()
    last = data[str(user_id)]["last_missao"]
    if last:
        last_dt = datetime.fromisoformat(last)
        if now - last_dt < timedelta(hours=24):
            return "Você já completou a missão de hoje!"
    xp_bonus = random.randint(20, 50)
    coin_bonus = random.randint(30, 70)
    add_xp(user_id, xp_bonus)
    add_coins(user_id, coin_bonus)
    data[str(user_id)]["last_missao"] = now.isoformat()
    save_data()
    return f"Missão diária completada! Ganhou {xp_bonus} XP e {coin_bonus} coins!"

def minerar(user_id):
    xp_gain = random.randint(10, 30)
    coins_gain = random.randint(20, 50)
    add_xp(user_id, xp_gain)
    add_coins(user_id, coins_gain)
    return f"Você minerou {coins_gain} coins e ganhou {xp_gain} XP!"

def saquear(user_id, target_id):
    init_user(user_id)
    init_user(target_id)
    if data[str(target_id)]["coins"] <= 0:
        return "O usuário não tem coins para saquear!"
    chance = 50
    if "espada" in data[str(user_id)]["inventory"]:
        chance += 15
    if "escudo" in data[str(target_id)]["inventory"]:
        chance -= 15
    chance = min(max(chance, 5), 95)
    roll = random.randint(1, 100)
    if roll <= chance:
        stolen = random.randint(1, min(50, data[str(target_id)]["coins"]))
        data[str(target_id)]["coins"] -= stolen
        data[str(user_id)]["coins"] += stolen
        save_data()
        return f"Sucesso! Você roubou {stolen} coins do usuário."
    else:
        return "Falhou no saque! Tente novamente mais tarde."

def perfil(user_id):
    init_user(user_id)
    u = data[str(user_id)]
    return f"Perfil:\nLevel: {u['level']}\nXP: {u['xp']}\nCoins: {u['coins']}\nItens: {', '.join(u['inventory']) if u['inventory'] else 'Nenhum'}"

def ver_loja():
    itens = [f"{item}: {preco} coins" for item, preco in loja.items()]
    return "Loja:\n" + "\n".join(itens)

def comprar(user_id, item):
    init_user(user_id)
    if item not in loja:
        return "Item não existe na loja!"
    preco = loja[item]
    if data[str(user_id)]["coins"] < preco:
        return "Você não tem coins suficientes!"
    data[str(user_id)]["coins"] -= preco
    data[str(user_id)]["inventory"].append(item)
    save_data()
    return f"Você comprou {item}!"

def vender(user_id, item):
    init_user(user_id)
    if item not in data[str(user_id)]["inventory"]:
        return "Você não possui esse item!"
    preco = loja.get(item, 10) // 2
    data[str(user_id)]["inventory"].remove(item)
    data[str(user_id)]["coins"] += preco
    save_data()
    return f"Você vendeu {item} por {preco} coins!"

def rank():
    ranking = sorted(data.items(), key=lambda x: (x[1]["level"], x[1]["coins"]), reverse=True)
    msg = "🏆 Ranking do grupo:\n"
    for i, (uid, u) in enumerate(ranking[:10], 1):
        msg += f"{i}. ID:{uid} - Level:{u['level']} XP:{u['xp']} Coins:{u['coins']}\n"
    return msg

# ===============================
# Boas-vindas automáticas e bloqueio de links
# ===============================
@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message):
    global welcome_active
    if not welcome_active:
        return
    for user in message.new_chat_members:
        init_user(user.id)
        add_xp(user.id, 10)
        add_coins(user.id, 50)
        bot.send_message(message.chat.id,
            f"🌸 Bem-vindo(a) {user.first_name}!\n"
            f"Você recebeu 10 XP e 50 coins de boas-vindas!\n"
            f"Use /dica para ver todos os comandos e /perfil para ver seu RPG."
        )

@bot.message_handler(func=lambda m: links_block_active and m.text and ("http://" in m.text or "https://" in m.text))
def block_links(message):
    bot.reply_to(message, "🚫 Links não são permitidos neste grupo! Usuário banido.")
    try:
        bot.kick_chat_member(message.chat.id, message.from_user.id)
    except:
        bot.reply_to(message, "Não foi possível banir o usuário (verifique permissões).")

# ===============================
# Comandos /start, /menu, /info, /dica
# ===============================
@bot.message_handler(commands=["start", "s"])
def cmd_start(message):
    user_id = message.from_user.id
    init_user(user_id)
    u = data[str(user_id)]
    start_text = f"""
🌸 Olá, {message.from_user.first_name}! Bem-vindo(a) ao KaoriBot 🌸

🎮 Seu perfil inicial:
├ Level: {u['level']}
├ XP: {u['xp']}
├ Coins: {u['coins']}
├ Itens: {', '.join(u['inventory']) if u['inventory'] else 'Nenhum'}

💡 Comandos úteis para começar:
├ /menu → Ver o menu completo
├ /dica → Aprender como usar cada comando
├ /perfil → Ver suas stats e inventário
├ /fig → Criar figurinhas

Divirta-se explorando jogos, RPG, moderação e diversão! 🌟
"""
    bot.reply_to(message, start_text)

@bot.message_handler(commands=["menu"])
def cmd_menu(message):
    menu_text = f"""
╭━━━━━━━━━━━━━━━🌸 KAORI BOT 🌸━━━━━━━━━━━━━━━╮
👤 Usuário
├ /start (s) → Iniciar o bot
├ /id → Ver seu ID
├ /perfil → Ver seu perfil RPG
├ /avatar → Ver avatar
├ /menu → Abrir menu completo
├ /info → Informações detalhadas do bot
├ /dica → Como usar todos os comandos
├ /prefixo → Mostra os atalhos e prefixos do bot
├ /fig → Criar figurinhas

🎮 Diversão & Jogos
├ /numero (n) → Número aleatório
├ /repetir (rm) → Repetir mensagem
├ /resposta (r) → Resposta aleatória
├ /forca (f) → Jogo da forca
├ /caraoucoroa (c) → Cara ou coroa
├ /rolardado (ro) → Rolar dado grande
├ /piada (p) → Contar piada
├ /quiz (q) → Quiz aleatório

🎲 RPG & Economia
├ /perfil → Stats, coins e inventário
├ /daily (d) → Recompensa diária
├ /missao → Missão diária
├ /rank → Ranking de XP e coins
├ /saquear @usuario → Roubar coins
├ /minerar → Ganhar coins e XP
├ /loja → Ver itens da loja
├ /comprar [item] → Comprar item
├ /vender [item] → Vender item

🛡 Moderação & Administração
├ /pin → Fixar mensagem
├ /unpin → Desafixar mensagem
├ /ban → Banir usuário
├ /kick → Expulsar usuário
├ /mute → Silenciar usuário
├ /unmute → Liberar usuário silenciado
├ /ativarbemvindo (abv) → Ativar mensagem de boas-vindas
├ /desativarbemvindo (dbv) → Desativar mensagem de boas-vindas
├ /ativarlinks (al) → Ativar bloqueio de links
├ /desativarlinks (dl) → Desativa bloqueio de links

🤖 Bot & Status
├ /status → Status completo do bot
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.reply_to(message, menu_text)

@bot.message_handler(commands=["info"])
def cmd_info(message):
    info_text = f"""
╭━━━━━━━━━━━━━━━🌸 INFORMAÇÕES KAORI BOT 🌸━━━━━━━━━━━━━━━╮
🤖 Nome: KaoriBot
🧠 Versão: v2.0 – RPG & Diversão Integrados
👤 Criador: Nikuu
🌐 Funcionalidades:
├ Comandos básicos e diversão
├ Sistema RPG com XP, coins, itens, loja e missões
├ Moderação de grupos (ban/kick/mute/unmute)
├ Bloqueio de links e mensagem de boas-vindas
├ Mini jogos: forca, cara ou coroa, rolar dados, quizzes
💎 Especial:
├ Criador inicia com 15.000 coins
├ Itens podem dar bônus em XP e coins
└ Saques e mineração com chances aleatórias
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.reply_to(message, info_text)

@bot.message_handler(commands=["dica"])
def cmd_dica(message):
    dica_text = f"""
╭━━━━━━━━━━━━━━🌸 GUIA DE COMANDOS KAORI BOT 🌸━━━━━━━━━━━━━━╮
👤 Usuário
├ /start (s) → Inicia o bot e ativa seu perfil RPG
├ /id → Mostra seu ID no Telegram
├ /perfil → Mostra seu perfil RPG (Level, XP, coins e inventário)
├ /avatar → Mostra sua foto de perfil
├ /menu → Mostra o menu completo
├ /info → Detalhes sobre o bot
├ /prefixo → Mostra atalhos
├ /fig → Cria figurinhas

🎮 Diversão & Jogos
├ /numero (n) → Número aleatório
├ /repetir (rm) → Repete a mensagem enviada
├ /resposta (r) → Responde aleatoriamente à sua pergunta
├ /forca (f) → Joga o jogo da forca
├ /caraoucoroa (c) → Cara ou coroa
├ /rolardado (ro) → Rola um dado grande
├ /piada (p) → Conta uma piada aleatória
├ /quiz (q) → Pergunta de quiz

🎲 RPG & Economia
├ /perfil → Stats, coins e inventário
├ /daily (d) → Recompensa diária
├ /missao → Missão diária
├ /rank → Ranking
├ /saquear @usuario → Roubar coins
├ /minerar → Ganhar coins e XP
├ /loja → Ver itens
├ /comprar [item] → Comprar item
├ /vender [item] → Vender item

🛡 Moderação & Administração
├ /pin → Fixar mensagem
├ /unpin → Desafixar mensagem
├ /ban → Banir usuário
├ /kick → Expulsar usuário
├ /mute → Silenciar usuário
├ /unmute → Liberar usuário
├ /ativarbemvindo (abv) → Ativar boas-vindas
├ /desativarbemvindo (dbv) → Desativar boas-vindas
├ /ativarlinks (al) → Ativar bloqueio de links
├ /desativarlinks (dl) → Desativar bloqueio de links
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    bot.reply_to(message, dica_text)

# ===============================
# Rodar bot
# ===============================
bot.infinity_polling()