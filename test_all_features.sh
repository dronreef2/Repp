#!/bin/bash

echo "=== Testing AI Learning Assistant v2.0 ==="
echo ""

echo "1. Testing Root Endpoint (GET /)"
curl -s http://localhost:5000/ | python -m json.tool
echo ""

echo "2. Testing POST /api/ask with level='universitário'"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "topic": "Machine Learning", "level": "universitário"}' \
  | python -m json.tool
echo ""

echo "3. Testing POST /api/ask with default level='básico'"
curl -s -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "topic": "Web Development"}' \
  | python -m json.tool
echo ""

echo "4. Testing GET /api/get_history"
curl -s "http://localhost:5000/api/get_history?user_id=test_user" | python -m json.tool
echo ""

echo "5. Testing GET /api/report (Analytical Report)"
curl -s "http://localhost:5000/api/report?user_id=test_user" | python -m json.tool
echo ""

echo "6. Testing Rate Limiting (5 requests per minute)"
for i in {1..6}; do
  echo "Request $i:"
  curl -s -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d "{\"user_id\": \"rate_limit_test\", \"topic\": \"Test $i\"}" \
    -w "\nHTTP Status: %{http_code}\n\n"
  sleep 0.5
done

echo "=== All Tests Completed ==="
