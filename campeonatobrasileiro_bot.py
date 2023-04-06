def campeonatobrasileiro_bot():
  # Checa no Telegram se há novas mensagens
  # Coloca as novas mensagens em uma lista "chats"
  for chat in chats:
    nova_mensagem = {"chat_id": chat_id, "text": message}
    requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    
    if message == "oi":
        texto_resposta = "Olá! Seja bem-vindo(a). Qual time você gostaria de saber os resultados na temporada?"
    elif message in ['Palmeiras', 'Flamengo', 'Corinthians', 'Sao Paulo', 'Atletico Mineiro', 'Internacional', 'Ceara', 'Bahia', 'Athletico Paranaense', 'Chapecoense', 'Cuiaba', 'Fluminense', 'Santos', 'America-MG', 'Gremio', 'Fortaleza', 'Sport', 'Red Bull Bragantino', 'Juventude', 'Atletico-GO']:
        df = pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/raw/main/Jogos_Temporada_2021_SerieAB.xlsx')
        #dffiltrado = df[(df.mandante == message) | (df.visitante == message)]
        dffiltrado = df[(df.Mandante == message) | (df.Visitante == message)]
        #texto_resposta = f"Aqui estão os resultados do {message} na temporada:\n{dffiltrado.to_string(index=False)}"
        texto_resposta = []
        jogos = dffiltrado.to_dict('records')
        for jogo in jogos:
            texto_resposta.append(str(jogo).replace('{', '').replace("'",'').replace(',','\n'))
    else:
        #texto_resposta = "Não entendi! Diga /start para começar."
        texto_resposta = "Não entendi! Diga 'oi' para começar."
  
    #nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
    #requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    if type(texto_resposta) == list:
        texto = f'Vamos enviar uma mensagem para cada jogo do {message}'
        nova_mensagem = {"chat_id": chat_id, "text": texto}
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
        for jogo in texto_resposta:
            nova_mensagem = {"chat_id": chat_id, "text": jogo}
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    else:
        nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    
    return "ok"

  
campeonatobrasileiro_bot()  
