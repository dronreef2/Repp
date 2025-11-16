import os
import time
import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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

def get_user_id_from_request():
    if request.is_json:
        data = request.get_json(silent=True)
        return data.get('user_id', get_remote_address()) if data else get_remote_address()
    return get_remote_address()

limiter = Limiter(
    app=app,
    default_limits=[],
    storage_uri="memory://",
    key_func=get_user_id_from_request
)

@app.route('/')
def home():
    return jsonify({
        "name": "Agente Assistivo de Aprendizagem",
        "version": "2.0.0",
        "features": ["AI Learning Assistant", "Progress Reports", "Rate Limiting", "Level Personalization"]
    })

@app.route('/api/ask', methods=['POST'])
@limiter.limit("5 per minute")
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
    level = data.get('level', 'básico')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    if not topic:
        return jsonify({"error": "topic is required"}), 400
    
    timestamp = int(time.time())
    key = f"query:{user_id}:{timestamp}"
    
    db[key] = json.dumps({
        "user_id": user_id,
        "topic": topic,
        "level": level,
        "timestamp": timestamp
    })
    
    response = integrar_gemini(topic, level)
    
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

@app.route('/api/report', methods=['GET'])
def report():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    prefix = f"query:{user_id}"
    history_list = []
    
    for key in db.prefix(prefix):
        try:
            data = json.loads(db[key])
            history_list.append(data['topic'])
        except (json.JSONDecodeError, KeyError):
            continue
    
    if not history_list:
        return jsonify({
            "analysis_summary": "Nenhum histórico de aprendizagem encontrado para este usuário.",
            "focus_areas": [],
            "recommendation": "Comece fazendo perguntas sobre tópicos de seu interesse para construir seu histórico de aprendizagem."
        }), 200
    
    report_data = gerar_relatorio_analitico(history_list)
    
    return jsonify(report_data), 200

def integrar_gemini(topic: str, level: str = 'básico') -> dict:
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.7,
            }
        )
        
        level_instructions = {
            'básico': "Use linguagem simples e acessível, como se estivesse explicando para alguém sem conhecimento prévio do assunto.",
            'intermediário': "Use linguagem técnica moderada, assumindo conhecimento básico do assunto.",
            'universitário': "Use linguagem acadêmica e aprofundada, com conceitos técnicos avançados e rigor científico.",
            'avançado': "Use linguagem especializada, assumindo expertise no domínio e incluindo nuances técnicas complexas."
        }
        
        level_instruction = level_instructions.get(level, level_instructions['básico'])
        
        prompt = f"""Você é um Agente Assistivo de Aprendizagem. Sua tarefa é fornecer uma explicação concisa e fácil de entender (cerca de 100 palavras) sobre o tópico fornecido.

Nível do usuário: {level}
Ajuste de tom: {level_instruction}

Tópico: {topic}

Sua resposta deve ser EXCLUSIVAMENTE no formato JSON com a seguinte estrutura:
{{
  "summary": "Explicação concisa do tópico ajustada ao nível {level}",
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

def gerar_relatorio_analitico(historico_list: list) -> dict:
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.7,
            }
        )
        
        topics_text = ", ".join(historico_list)
        
        prompt = f"""Você é um Analista de Aprendizagem Educacional. Analise o histórico de consultas do usuário e forneça feedback personalizado e motivacional.

Histórico de tópicos consultados: {topics_text}

Sua tarefa:
1. Analise a diversidade de temas e identifique padrões
2. Categorize as principais áreas de foco do usuário
3. Gere uma recomendação motivacional e construtiva

Sua resposta deve ser EXCLUSIVAMENTE no formato JSON com a seguinte estrutura:
{{
  "analysis_summary": "Resumo analítico da jornada de aprendizagem, destacando a diversidade ou especialização dos tópicos",
  "focus_areas": ["Área de foco 1", "Área de foco 2"],
  "recommendation": "Recomendação personalizada e motivacional para continuar a jornada de aprendizagem"
}}

Retorne apenas o JSON, sem texto adicional."""
        
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        
        if 'analysis_summary' not in result or 'focus_areas' not in result or 'recommendation' not in result:
            raise ValueError("Invalid response structure")
        
        return result
        
    except Exception as e:
        app.logger.error(f"Erro ao gerar relatório: {type(e).__name__}: {str(e)}")
        return {
            "analysis_summary": f"Você consultou {len(historico_list)} tópicos até agora, demonstrando curiosidade e busca por conhecimento.",
            "focus_areas": list(set(historico_list[:3])),
            "recommendation": "Continue explorando novos tópicos e aprofundando seu conhecimento nas áreas de seu interesse."
        }

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Você excedeu o limite de 5 requisições por minuto. Por favor, aguarde um momento antes de tentar novamente."
    }), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
