import os
import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
import pandas as pd
import openpyxl

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1ZDyxhXlCtCjMbyKvYmMt_8jAKN5JSoZ7x3MqlnoyzAM")
sheet = planilha.worksheet("Sheet1")
app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/campeonato brasileiro">Campeonato Brasileiro</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Bem Vindo! Esse site vai te ajudar com dados sobre o Campeonato Brasileiro."

@app.route("/sobre")
def sobre():
  return menu + "Aqui você encontra dados sobre todas as temporadas do campeonato Brasileiro que foram disponibilizados pela CBF"

@app.route("/contato")
def contato():
  return menu + "Para saber mais detalhes, mande um oi no usuário Dados Campeonato Brasileiro, no Telegram"

@app.route("/campeonato-brasileiro")
def campeonato_brasileiro():
  pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/raw/main/Jogos_Temporada_2021_SerieAB.xlsx')
  return df.to_html()

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Sérgio", "Vieira", "a partir do Flask"])
  return "Planilha escrita!"

@app.route("/campeonatobrasileiro-bot", methods=["POST"])
def campeonatobrasileiro_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]
    #nova_mensagem = {"chat_id": chat_id, "text": message}
    #requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    
    #if message == "/start":
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

#####

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




