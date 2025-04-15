from flask import Flask, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")  # você vai adicionar essa variável depois

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
