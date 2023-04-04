from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
   return "Bem vindo! Este site contém informações sobre o Campeonato Brasileiro"
