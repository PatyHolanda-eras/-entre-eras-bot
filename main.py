from flask import Flask, request
import openai
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Está vivo!"


openai.api_key = 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 # você vai adicionar essa variável depois

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form  # twilio envia como form, não json
    mensagem = data.get('Body', '')

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": mensagem}]
    )

    texto = resposta['choices'][0]['message']['content']
    return texto

app.run(host='0.0.0.0', port=81)
