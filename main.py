from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Está vivo!"

# Pegando a API key do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form  # o Twilio envia como form-urlencoded
    mensagem = data.get('Body', '')

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": mensagem}]
    )

    texto = resposta['choices'][0]['message']['content']

    # Resposta em XML (TwiML) que o WhatsApp/Twilio entende
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto}</Message>
</Response>"""

    return Response(twiml_response, mimetype='text/xml')

app.run(host='0.0.0.0', port=81)
