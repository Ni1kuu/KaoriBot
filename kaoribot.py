import telebot import random import os import time from io import BytesIO

===============================

CONFIGURAÇÕES

===============================

TOKEN = os.environ.get("TOKEN") CREATOR_ID = int(os.environ.get("7659474646")) bot = telebot.TeleBot(TOKEN)

welcome_active = True links_block_active = False

===============================

BOAS-VINDAS E BLOQUEIO DE LINKS

===============================

@bot.message_handler(content_types=['new_chat_members']) def welcome_new_member(message): if welcome_active: for user in message.new_chat_members: bot.send_message(message.chat.id,f"🌸 Bem-vindo(a) {user.first_name}! Use /dica para ver todos os comandos.")

@bot.message_handler(func=lambda m: links_block_active and m.text and ('http://' in m.text or 'https://' in m.text)) def block_links(message): bot.reply_to(message,"🚫 Links não são permitidos! Usuário banido.") try: bot.kick_chat_member(message.chat.id,message.from_user.id) except: bot.reply_to(message,"Não foi possível banir o usuário (permissão insuficiente).")

===============================

COMANDOS BÁSICOS

===============================

@bot.message_handler(commands=['start','s']) def cmd_start(message): bot.reply_to(message,f"🌸 Olá, {message.from_user.first_name}!\nUse /menu para ver todos os comandos disponíveis.")

@bot.message_handler(commands=['menu']) def cmd_menu(message): menu_text=""" ╭━━━🌸 MENU KAORI BOT 🌸━━━╮ 👤 Usuário /start → Iniciar bot (atalho: /s) /id → Ver seu ID /perfil → Ver seu perfil /avatar → Ver avatar /menu → Abrir menu completo /info → Informações do bot /dica → Mostra como usar os comandos /prefixo → Mostra os atalhos e prefixos do bot /fig → Cria figurinhas 🎮 Diversão & Jogos /numero → Número aleatório (atalho: /n) /repetir → Repetir mensagem (atalho: /rm) /resposta → Resposta aleatória (atalho: /r) /forca → Brincadeiras (Forca) (atalho: /f) /caraoucoroa → Cara ou coroa (atalho: /c) /rolardado → Rolar dado grande (atalho: /ro) /piada → Contar piada (atalho: /p) /quiz → Quiz aleatório (atalho: /q) 🛡 Moderação / Administração /pin → Fixar mensagem respondida /unpin → Desafixar mensagem /ban → Banir usuário do grupo /kick → Expulsar usuário do grupo /mute → Silenciar usuário /unmute → Liberar usuário silenciado /ativarbemvindo → Ativar mensagem de boas-vindas (abv) /desativarbemvindo → Desativar mensagem de boas-vindas (dbv) /ativarlinks → Ativar bloqueio de links (ban automático) (al) /desativarlinks → Desativar bloqueio de links (dl) 🤖 Bot & Status /status → Status completo /ping → Verificar se estou online ╰━━━━━━━━━━━━━━━━━━━━╯""" bot.reply_to(message,menu_text)

@bot.message_handler(commands=['info']) def cmd_info(message): bot.reply_to(message,"🤖 KaoriBot v2.5\nCriador: Nikuu\nFunções: Diversão, moderação, mini jogos e figurinhas fofinhas! 🌸")

@bot.message_handler(commands=['dica']) def cmd_dica(message): dica_text=""" Use os comandos como estão listados no menu. Atalhos entre parênteses. 🎮 Diversão & Jogos /numero (n) → Número aleatório /repetir (rm) → Repete mensagem /resposta (r) → Resposta aleatória /forca (f) → Jogo da forca /caraoucoroa (c) → Cara ou coroa /rolardado (ro) → Rola um dado grande /piada (p) → Contar piada /quiz (q) → Quiz aleatório 🛡 Moderação & Administração /pin → Fixar mensagem /unpin → Desafixar /ban → Banir /kick → Expulsar /mute → Silenciar /unmute → Liberar /ativarbemvindo (abv) → Ativar boas-vindas /desativarbemvindo (dbv) → Desativar boas-vindas /ativarlinks (al) → Ativar bloqueio de links /desativarlinks (dl) → Desativar bloqueio de links 🤖 Bot & Status /status → Status completo /ping → Ver ping fofo do bot /fig → Cria figurinhas enviando uma foto antes do comando """ bot.reply_to(message,dica_text)

@bot.message_handler(commands=['prefixo']) def cmd_prefixo(message): bot.reply_to(message,"Todos os comandos possuem atalhos entre parênteses no menu. Ex: /start (s), /numero (n)")

===============================

Diversão & Jogos

===============================

@bot.message_handler(commands=['numero','n']) def cmd_numero(message): bot.reply_to(message,f"🎲 Número aleatório: {random.randint(0,100)}")

@bot.message_handler(commands=['repetir','rm']) def cmd_repetir(message): text=message.text.split(' ',1) if len(text)>1: bot.reply_to(message,text[1]) else: bot.reply_to(message,"📌 Use /repetir [mensagem]")

@bot.message_handler(commands=['resposta','r']) def cmd_resposta(message): respostas=["Sim! 🌸","Não! 😢","Talvez 🤔","Claro! 😎","Jamais! 💀"] bot.reply_to(message,random.choice(respostas))

@bot.message_handler(commands=['caraoucoroa','c']) def cmd_caraoucoroa(message): bot.reply_to(message,f"🪙 {'Cara' if random.randint(0,1)==0 else 'Coroa'}")

@bot.message_handler(commands=['rolardado','ro']) def cmd_rolardado(message): bot.reply_to(message,f"🎲 Resultado do dado: {random.randint(1,20)}")

@bot.message_handler(commands=['piada','p']) def cmd_piada(message): piadas=["Por que o computador foi ao médico? Porque pegou um vírus! 😆","O que é um pontinho amarelo na estrada? Um milho atropelado! 🌽"] bot.reply_to(message,random.choice(piadas))

@bot.message_handler(commands=['quiz','q']) def cmd_quiz(message): quizzes=["Qual a cor do céu? Resposta: Azul 🌌","Quanto é 2+2? Resposta: 4 🧮"] bot.reply_to(message,random.choice(quizzes))

===============================

Figurinhas

===============================

last_photo = {}

@bot.message_handler(content_types=['photo']) def handle_photo(message): last_photo[message.from_user.id] = message.photo[-1].file_id bot.reply_to(message, "🌸 Foto recebida! Agora use /fig para transformar em figurinha.")

@bot.message_handler(commands=['fig']) def cmd_fig(message): user_id = message.from_user.id if user_id not in last_photo: bot.reply_to(message, "📌 Envie uma foto antes de usar /fig") return file_id = last_photo[user_id] bot.send_sticker(message.chat.id, file_id)

===============================

Bot & Status

===============================

@bot.message_handler(commands=['status']) def cmd_status(message): bot.reply_to(message,"🤖 Estou online! 🌸")

@bot.message_handler(commands=['ping']) def cmd_ping(message): start_time=time.time() msg=bot.send_message(message.chat.id,"🏓 Pingando... 🐾") end_time=time.time() ping_ms=int((end_time-start_time)*1000) bot.edit_message_text(f"🏓 Pong fofo! {ping_ms}ms 🌸",message.chat.id,msg.message_id)

===============================

Moderação / Administração

===============================

@bot.message_handler(commands=['ativarbemvindo','abv']) def cmd_ativar_bemvindo(message): global welcome_active welcome_active=True bot.reply_to(message,"🌸 Boas-vindas ativadas!")

@bot.message_handler(commands=['desativarbemvindo','dbv']) def cmd_desativar_bemvindo(message): global welcome_active welcome_active=False bot.reply_to(message,"🌸 Boas-vindas desativadas!")

@bot.message_handler(commands=['ativarlinks','al']) def cmd_ativar_links(message): global links_block_active links_block_active=True bot.reply_to(message,"🚫 Bloqueio de links ativado!")

@bot.message_handler(commands=['desativarlinks','dl']) def cmd_desativar_links(message): global links_block_active links_block_active=False bot.reply_to(message,"🚫 Bloqueio de links desativado!")

===============================

Rodando o bot

===============================

bot.infinity_polling()