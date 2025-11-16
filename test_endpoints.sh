#!/bin/bash

echo "======================================"
echo "TESTE DO AGENTE ASSISTIVO DE APRENDIZAGEM"
echo "======================================"
echo ""

echo "1. Testando endpoint raiz GET /"
curl -s http://localhost:5000/
echo -e "\n"

echo "2. Testando POST /api/ask com dados válidos"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "estudante_1", "topic": "Inteligência Artificial"}' | python -m json.tool
echo -e "\n"

echo "3. Testando erro 400: Content-Type incorreto"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: text/plain" \
  -d '{"user_id": "test", "topic": "test"}'
echo -e "\n"

echo "4. Testando erro 400: JSON malformado"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d 'invalid json'
echo -e "\n"

echo "5. Testando erro 400: Campo user_id ausente"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"topic": "test"}'
echo -e "\n"

echo "6. Testando erro 400: Campo topic ausente"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test"}'
echo -e "\n"

echo "7. Criando múltiplas consultas para testar histórico"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "aluno_teste", "topic": "Python"}' > /dev/null
sleep 1
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "aluno_teste", "topic": "JavaScript"}' > /dev/null
sleep 1
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "aluno_teste", "topic": "Rust"}' > /dev/null
echo "Consultas criadas"
echo ""

echo "8. Testando GET /api/get_history com user_id válido"
curl -s "http://localhost:5000/api/get_history?user_id=aluno_teste" | python -m json.tool
echo -e "\n"

echo "9. Testando erro 400: user_id ausente no histórico"
curl -s "http://localhost:5000/api/get_history"
echo -e "\n"

echo "======================================"
echo "TODOS OS TESTES CONCLUÍDOS"
echo "======================================"
