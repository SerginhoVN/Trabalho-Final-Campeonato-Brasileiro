import os

import gspread
import requests
from flask import Flask
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper


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


def ultimas_promocoes():
  scraper = ChannelScraper()
  contador = 0
  resultado = []
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    resultado.append(f"{message.created_at} {texto}")
    if contador == 10:
      return resultado

    
menu = """
<a href="/">Página inicial</a> | <a href="/promocoes">PROMOÇÕES</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
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


@app.route("/Campeonato Brasileiro")
def campeonato():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/campeonatobrasileiro_bot">@campeontobrasileiro_bot</a>:
  <br>
  <ul>
  """
  for campbrasil in campeonato():
    conteudo += f"<li>{campbrasil}</li>"
  return conteudo + "</ul>"


@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"


@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Sérgio", "Vieira", "a partir do Flask"])
  return "Planilha escrita!"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id": chat_id, "text": message}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"
