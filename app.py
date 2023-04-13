import os
import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import openpyxl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

SENDGRID_KEY = os.environ["API_SENDGRID"]
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)

#Planilhas do bot Campeonato Brasileiro do Telegram
planilha = api.open_by_key("14jvq5dfYVerz8V_xyYIa0DEkSjz1DgwWQcHM7BsOcys")
sheet = planilha.worksheet("CampeonatoBrasileiro")
app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | 
<a href="/campeonato-brasileiro/2021">Campeonato Brasileiro 2021 </a> | 
<a href="/campeonato-brasileiro/2020">Campeonato 2020 </a> | 
<a href="/campeonato-brasileiro/2019">Campeonato 2019 </a> | 
<a href="/campeonato-brasileiro/2018">Campeonato 2018 </a> | 
<a href="/campeonato-brasileiro/2017">Campeonato 2017 </a> | 
<a href="/campeonato-brasileiro/2016">Campeonato 2016 </a> |
<a href="/campeonato-brasileiro/2015">Campeonato 2015 </a> |  
<a href="/campeonato-brasileiro/2014">Campeonato 2014 </a> | 
<a href="/campeonato-brasileiro/2013">Campeonato 2013 </a> | 
<a href="/campeonato-brasileiro/2012">Campeonato 2012 </a> | 
<a href="/campeonato-brasileiro/2011">Campeonato 2011 </a> | 
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

@app.route("/campeonato-brasileiro/<ano>")
def campeonato_brasileiro(ano):
  df = pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/raw/main/Jogos_Temporada_%20Todas%20as%20Temporadas_SerieAB.xlsx', engine='openpyxl')
  df = df[df["Temporada"] == int(ano)]
  html = f"<h1>{ano}</h1>"
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
  message = update["message"]["text"]
 
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
     
  if message == "oi":
      texto_resposta = "Olá! Seja bem-vindo(a). Qual time você gostaria de saber os resultados na temporada?"
     
  elif message in times:
      df = pd.read_excel('https://github.com/SerginhoVN/Trabalho-Final-Campeonato-Brasileiro/raw/main/Jogos_Temporada_%20Todas%20as%20Temporadas_SerieAB.xlsx')
      dffiltrado = df[(df.Mandante == message) | (df.Visitante == message)]
      atual = dffiltrado["Temporada"].max()
      dffiltrado = dffiltrado[dffiltrado["Temporada"] == atual]
      texto_resposta_time = f"Aqui estão os resultados do {message} na temporada {atual}:\n\n" 
      jogos = dffiltrado.to_dict('records')
    
      for jogo in jogos:
        texto_resposta_time += f"Rodada: {jogo['Rodada']} - {jogo['Mandante']} {jogo['Placar']} {jogo['Visitante']}\n"
        texto_resposta_time += f"Quer receber por email? informe seu email."
    
  elif "@" in message:
      texto_resposta = "Obrigado! Vamos te cadastrar para receber as informações solicitadas"
      email = Mail(
      from_email='serginhosp21@gmail.com',
      to_emails=message,
      subject='Campeonato Brasileiro',
      html_content = texto_resposta_time
      )
      sg = SendGridAPIClient(SENDGRID_KEY)
      response = sg.send(email)
   
  else:
      texto_resposta = "Não entendi! Diga 'oi' para começar."

  if texto_resposta_time:
      texto_resposta = texto_resposta_time 
  
      nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
      requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
      mensagens.append([datahora, "enviada", first_name, chat_id, texto_resposta])
      sheet.append_row([datahora, first_name, chat_id, message])  
  return "ok"

#Sendgrid
@app.route("/send-email")
def send_email():
    emails=[]
    respostas = sheet.col_values(4)
    return "ok"
