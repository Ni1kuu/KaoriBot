import telebot import random import json import time import threading import os from datetime import datetime, timedelta

===============================

CONFIGURAÇÕES

===============================

TOKEN = os.environ.get("TOKEN") CREATOR_ID = int(os.environ.get("7659474646")) bot = telebot.TeleBot(TOKEN)

welcome_active = True links_block_active = False

===============================

Dados RPG e Usuários

===============================

try: with open("rpg_data.json","r") as f: data = json.load(f) except FileNotFoundError: data = {}

SAVE_INTERVAL = 10

def save_periodic(): while True: time.sleep(SAVE_INTERVAL) with open("rpg_data.json","w") as f: json.dump(data,f,indent=4) print("💾 Dados RPG salvos...")

threading.Thread(target=save_periodic,daemon=True).start()

===============================

Funções gerais

===============================

def init_user(user_id): if str(user_id) not in data: data[str(user_id)] = { "xp":0, "level":0, "coins":15000 if user_id==CREATOR_ID else 0, "last_daily":None, "last_missao":None, "inventory":[] }

def add_xp(user_id,amount): init_user(user_id) data[str(user_id)]['xp']+=amount while data[str(user_id)]['xp'] >= (data[str(user_id)]['level']+1)*100: data[str(user_id)]['xp']-=(data[str(user_id)]['level']+1)*100 data[str(user_id)]['level']+=1

def add_coins(user_id,amount): init_user(user_id) data[str(user_id)]['coins']+=amount

===============================

RPG / Economia

===============================

loja={"espada":100,"escudo":80,"poção":50,"amuleto":200,"moedinha":150}

def daily(user_id): init_user(user_id) now=datetime.now() last=data[str(user_id)]['last_daily'] if last: last_dt=datetime.fromisoformat(last) if now-last_dt<timedelta(hours=24): return f"Você já pegou sua recompensa diária! Volte em {24-(now-last_dt).seconds//3600}h." reward=random.randint(50,150) add_coins(user_id,reward) data[str(user_id)]['last_daily']=now.isoformat() return f"Você recebeu {reward} coins no /daily!"

def missao(user_id): init_user(user_id) now=datetime.now() last=data[str(user_id)]['last_missao'] if last: last_dt=datetime.fromisoformat(last) if now-last_dt<timedelta(hours=24): return "Você já completou a missão de hoje!" xp_bonus=random.randint(20,50) coin_bonus=random.randint(30,70) add_xp(user_id,xp_bonus) add_coins(user_id,coin_bonus) data[str(user_id)]['last_missao']=now.isoformat() return f"Missão diária completada! Ganhou {xp_bonus} XP e {coin_bonus} coins!"

def minerar(user_id): xp_gain=random.randint(10,30) coins_gain=random.randint(20,50) add_xp(user_id,xp_gain) add_coins(user_id,coins_gain) return f"Você minerou {coins_gain} coins e ganhou {xp_gain} XP!"

def saquear(user_id,target_id): init_user(user_id) init_user(target_id) if data[str(target_id)]['coins']<=0: return "O usuário não tem coins para saquear!" chance=50 roll=random.randint(1,100) if roll<=chance: stolen=random.randint(1,min(50,data[str(target_id)]['coins'])) data[str(target_id)]['coins']-=stolen data[str(user_id)]['coins']+=stolen return f"Sucesso! Você roubou {stolen} coins do usuário." else: return "Falhou no saque! Tente novamente mais tarde."

def perfil(user_id): init_user(user_id) u=data[str(user_id)] return f"Perfil:\nLevel: {u['level']}\nXP: {u['xp']}\nCoins: {u['coins']}\nItens: {', '.join(u['inventory']) if u['inventory'] else 'Nenhum'}"

def ver_loja(): return "Loja:\n"+"\n".join([f"{k}: {v} coins" for k,v in loja.items()])

def comprar(user_id,item): init_user(user_id) if item not in loja: return "Item não existe na loja!" if data[str(user_id)]['coins']<loja[item]: return "Você não tem coins suficientes!" data[str(user_id)]['coins']-=loja[item] data[str(user_id)]['inventory'].append(item) return f"Você comprou {item}!"

def vender(user_id,item): init_user(user_id) if item not in data[str(user_id)]['inventory']: return "Você não possui esse item!" preco=loja.get(item,10)//2 data[str(user_id)]['inventory'].remove(item) data[str(user_id)]['coins']+=preco return f"Você vendeu {item} por {preco} coins!"

def rank(): ranking=sorted(data.items(),key=lambda x:(x[1]['level'],x[1]['coins']),reverse=True) msg="🏆 Ranking do grupo:\n" for i,(uid,u) in enumerate(ranking[:10],1): msg+=f"{i}. ID:{uid} - Level:{u['level']} XP:{u['xp']} Coins:{u['coins']}\n" return msg

===============================

Boas-vindas e Links

===============================

@bot.message_handler(content_types=['new_chat_members']) def welcome_new_member(message): if not welcome_active: return for user in message.new_chat_members: init_user(user.id) add_xp(user.id,10) add_coins(user.id,50) bot.send_message(message.chat.id,f"🌸 Bem-vindo(a) {user.first_name}! Você recebeu 10 XP e 50 coins de boas-vindas! Use /dica para ver os comandos.")

@bot.message_handler(func=lambda m: links_block_active and m.text and ('http://' in m.text or 'https://' in m.text)) def block_links(message): bot.reply_to(message,"🚫 Links não são permitidos! Usuário banido.") try: bot.kick_chat_member(message.chat.id,message.from_user.id) except: bot.reply_to(message,"Não foi possível banir o usuário (permissão insuficiente).")

===============================

Comandos básicos, RPG e Diversão

===============================

@bot.message_handler(commands=['start','s']) def cmd_start(message): user_id=message.from_user.id init_user(user_id) u=data[str(user_id)] bot.reply_to(message,f"🌸 Olá, {message.from_user.first_name}!\n🎮 Level: {u['level']}, XP: {u['xp']}, Coins: {u['coins']}, Itens: {', '.join(u['inventory']) if u['inventory'] else 'Nenhum'}\nUse /menu para ver todos os comandos!")

@bot.message_handler(commands=['menu']) def cmd_menu(message): menu_text=""" ╭━━━🌸 MENU KAORI BOT 🌸━━━╮ 👤 Usuário /start → Iniciar bot (atalho: /s) /id → Ver seu ID /perfil → Ver seu perfil /avatar → Ver avatar /menu → Abrir menu completo /info → Informações do bot /dica → Mostra como usar os comandos /prefixo → Mostra os atalhos e prefixos do bot /fig → Cria figurinhas 🎮 Diversão & Jogos /numero → Número aleatório (atalho: /n) /repetir → Repetir mensagem (atalho: /rm) /resposta → Resposta aleatória (atalho: /r) /forca → Brincadeiras (Forca) (atalho: /f) /caraoucoroa → Cara ou coroa (atalho: /c) /rolardado → Rolar dado grande (atalho: /ro) /piada → Contar piada (atalho: /p) /quiz → Quiz aleatório (atalho: /q) 🛡 Moderação / Administração /pin → Fixar mensagem respondida /unpin → Desafixar mensagem /ban → Banir usuário do grupo /kick → Expulsar usuário do grupo /mute → Silenciar usuário /unmute → Liberar usuário silenciado /ativarbemvindo → Ativar mensagem de boas-vindas /desativarbemvindo → Desativar mensagem de boas-vindas /ativarlinks → Ativar bloqueio de links (ban automático) /desativarlinks → Desativar bloqueio de links 🤖 Bot & Status /status → Status completo /ping → Verificar se estou online ╰━━━━━━━━━━━━━━━━━━━━╯""" bot.reply_to(message,menu_text)

@bot.message_handler(commands=['ping']) def cmd_ping(message): start_time=time.time() msg=bot.send_message(message.chat.id,"🏓 Pingando... 🐾") end_time=time.time() ping_ms=int((end_time-start_time)*1000) bot.edit_message_text(f"🏓 Pong! Ping fofo: {ping_ms}ms 🌸",message.chat.id,msg.message_id)

@bot.message_handler(commands=['info']) def cmd_info(message): bot.reply_to(message,"🤖 KaoriBot v2.5 – Diversão + RPG Integrados\nCriador: Nikuu\nSistema de XP, coins, itens, loja, missão diária e saques!\nMini jogos: forca, cara ou coroa, rolar dados, quiz.")

@bot.message_handler(commands=['dica']) def cmd_dica(message): dica_text=""" Use os comandos exatamente como aparecem, atalhos entre parênteses. 🎮 Diversão & Jogos /numero (n) → Número aleatório /repetir (rm) → Repete mensagem /resposta (r) → Resposta aleatória /forca (f) → Jogo da forca /caraoucoroa (c) → Cara ou coroa /rolardado (ro) → Rola um dado grande /piada (p) → Contar piada /quiz (q) → Quiz aleatório 🎲 RPG & Economia /perfil → Stats, coins e inventário /daily (d) → Recompensa diária /missao → Missão diária /rank → Ranking /saquear @usuario → Roubar coins /minerar → Ganhar coins e XP /loja → Ver itens da loja /comprar [item] → Comprar item /vender [item] → Vender item 🛡 Moderação & Administração /pin → Fixar mensagem /unpin → Desafixar /ban → Banir /kick → Expulsar /mute → Silenciar /unmute → Liberar /ativarbemvindo (abv) → Ativar boas-vindas /desativarbemvindo (dbv) → Desativar boas-vindas /ativarlinks (al) → Ativar bloqueio de links /desativarlinks (dl) → Desativa bloqueio de links """ bot.reply_to(message,dica_text)

===============================

Inicia bot

===============================

bot.infinity_polling()