import os
import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
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
<a href="/">Página inicial</a> | 
<a href="/campeonato brasileiro/2021">Campeonato Brasileiro </a> | 
<a href="/sobre">Sobre</a> | 
<a href="/contato">Contato</a>
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

@app.route("/campeonato-brasileiro/2021")
def campeonato_brasileiro(ano):
  df = pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/raw/main/Jogos_Temporada_2021_SerieAB.xlsx')
  df = df[df["Temporada"] == int(ano)]
  
  html = f"<h1>{ano}<h/h'>"
  for ano in df["Temporada"].unique():
    html += f'<a href="/campeonato brasileiro/{ano}>{ano}<a/a> |'
    html += df.to_html()
  return html

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Sérgio", "Vieira", "a partir do Flask"])
  return "Planilha escrita!"

#Telegram

@app.route("/campeonatobrasileiro-bot", methods=["POST"])
def campeonatobrasileiro_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]  
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]
    
    #if message == "/start":
    if message == "oi":
        texto_resposta = "Olá! Seja bem-vindo(a). Qual time você gostaria de saber os resultados na temporada?"
    
    times = ['Palmeiras', 
             'Flamengo', 
             'Corinthians', 
             'Sao Paulo', 
             'Atletico Mineiro', 
             'Internacional', 
             'Ceara', 
             'Bahia', 
             'Athletico Paranaense', 
             'Chapecoense', 
             'Cuiaba', 
             'Fluminense', 
             'Santos', 
             'America-MG', 
             'Gremio', 
             'Fortaleza', 
             'Sport', 
             'Red Bull Bragantino', 
             'Juventude', 
             'Atletico-GO']
 
    elif message in times:
      df = pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/raw/main/Jogos_Temporada_2021_SerieAB.xlsx')
      dffiltrado = df[(df.Mandante == message) | (df.Visitante == message)]
      atual = dffiltrado["Temporada"].max()
      dffiltrado = dffiltrado[dffiltrado["Temporada"] == atual]
      texto_resposta = []
      jogos = dffiltrado.to_dict("records")
      
      for jogo in jogos:
        texto_resposta.append(str(jogo).replace('{', '').replace("'",'').replace(',','\n'))
        texto_resposta = f"Jogos do time {message}\n\n" + '\n'.join(texto_resposta)
          
        
    else:
      texto_resposta = "Não entendi! Diga 'oi' para começar."

nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem,)
    
return "ok"
