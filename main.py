from flask import Flask, request, Response
import openai
import os
import html

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Está vivo!"

# Pegando a API key do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.values  # mais seguro para lidar com diferentes tipos de envio
    mensagem = data.get('Body', '')

    if not mensagem:
        return Response("Mensagem vazia", status=400)

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem}]
        )
        texto = resposta['choices'][0]['message']['content']
    except Exception as e:
        texto = "Houve um erro ao processar sua mensagem. Tente novamente mais tarde."
        print(f"Erro na OpenAI: {e}")

    # Escapando caracteres especiais para evitar erros de XML
    texto_escapado = html.escape(texto)

    # Resposta em XML (TwiML)
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{texto_escapado}</Message>
</Response>"""

    return Response(twiml_response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
