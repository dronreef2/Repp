import os
import time
import json
from flask import Flask, request, jsonify
from replit import db
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    app.logger.warning("GEMINI_API_KEY não está configurada. A integração com IA não funcionará.")
else:
    genai.configure(api_key=api_key)

@app.route('/')
def home():
    return jsonify({
        "name": "Agente Assistivo de Aprendizagem",
        "version": "1.0.0"
    })

@app.route('/api/ask', methods=['POST'])
def ask():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Malformed JSON"}), 400
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    user_id = data.get('user_id')
    topic = data.get('topic')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    if not topic:
        return jsonify({"error": "topic is required"}), 400
    
    timestamp = int(time.time())
    key = f"query:{user_id}:{timestamp}"
    
    db[key] = json.dumps({
        "user_id": user_id,
        "topic": topic,
        "timestamp": timestamp
    })
    
    response = integrar_gemini(topic)
    
    return jsonify(response), 200

@app.route('/api/get_history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    prefix = f"query:{user_id}"
    history = []
    
    for key in db.prefix(prefix):
        try:
            data = json.loads(db[key])
            history.append((data['timestamp'], data['topic']))
        except (json.JSONDecodeError, KeyError):
            continue
    
    history.sort(reverse=True, key=lambda x: x[0])
    
    return jsonify({"history": history}), 200

def integrar_gemini(topic: str) -> dict:
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.7,
            }
        )
        
        prompt = f"""Você é um Agente Assistivo de Aprendizagem. Sua tarefa é fornecer uma explicação concisa e fácil de entender (cerca de 100 palavras) sobre o tópico fornecido.

Tópico: {topic}

Sua resposta deve ser EXCLUSIVAMENTE no formato JSON com a seguinte estrutura:
{{
  "summary": "Explicação concisa do tópico em cerca de 100 palavras",
  "next_steps": ["Primeiro próximo passo", "Segundo próximo passo", "Terceiro próximo passo"]
}}

Retorne apenas o JSON, sem texto adicional."""
        
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        
        if 'summary' not in result or 'next_steps' not in result:
            raise ValueError("Invalid response structure")
        
        return result
        
    except Exception as e:
        app.logger.error(f"Erro na integração Gemini: {type(e).__name__}: {str(e)}")
        return {
            "summary": f"Desculpe, ocorreu um erro ao processar o tópico '{topic}'. Por favor, tente novamente.",
            "next_steps": [
                "Verifique se a chave da API está configurada corretamente",
                "Tente reformular sua pergunta",
                "Entre em contato com o suporte se o problema persistir"
            ]
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
