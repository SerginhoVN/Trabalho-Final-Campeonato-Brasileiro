import os

import gspread
import requests
from flask import Flask
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
import pandas as pd

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


@app.route("/")
def index():
  return menu + "Bem Vindo! Esse site vai te ajudar com dados sobre o Campeonato Brasileiro."

@app.route("/sobre")
def sobre():
  return menu + "Aqui você encontra dados sobre todas as temporadas do campeonato Brasileiro que foram disponibilizados pela CBF"

@app.route("/contato")
def contato():
  return menu + "Para saber mais detalhes, mande um oi no usuário Dados Campeonato Brasileiro, no Telegram"


@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

#programando o Telegram 

@app.route("/campeonatobrasileiro-bot", methods=["POST"])
def campeonatobrasileiro_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]
    nova_mensagem = {"chat_id": chat_id, "text": message}
    requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  
    if message == "/start":  
        texto_resposta = "Olá! Seja bem-vinda(o). Você quer saber sobre qual time do Campeonato Brasileiro?"
    
    elif message in ['Palmeiras', 'Flamengo', 'Corinthians', 'Sao Paulo', 'Atletico Mineiro', 'Internacional', 'Ceara', 'Bahia', 'Athletico Paranaense', 'Chapecoense', 'Cuiaba', 'Fluminense', 'Palmeiras', 'Santos', 'America-MG', 'Gremio', 'Fortaleza', 'Sport', 'Red Bull Bragantino', 'Juventude', 'Atletico-GO']:
        texto_resposta = "Olá! Aqui estão os resultados do {message} na temporada"
        
       for message in df:
        df = pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/blob/main/Jogos_Temporada_2021_SerieAB.xlsx')
        dffiltrado = df[(df.mandante == message) | (df.visitante == message)]
        texto_resposta = f'{texto_resposta} \n \n{message}'
   
     else:
      texto_resposta = "Não entendi! Diga Oi e veja as últimas notícias da BR Aviation e Vibra"
         
  return "ok"


      #incluir pipedream para deixar recorrente 






