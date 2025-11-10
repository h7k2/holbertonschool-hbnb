#!/bin/bash

API_BASE="http://127.0.0.1:5000/api/v1"

echo "=== TEST ENDPOINTS DISPONIBLES ==="

# Tester la racine de l'API
echo "1. Test racine API..."
curl -s "$API_BASE" || curl -s "http://127.0.0.1:5000/"

echo -e "\n\n2. Test endpoints auth..."
curl -s "$API_BASE/auth/" || curl -s "$API_BASE/auth"

echo -e "\n\n3. Test création user (corrigé)..."
curl -X POST "$API_BASE/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Johnson", 
    "email": "test_'$(date +%s)'@example.com",
    "password": "Password123"
  }'

echo -e "\n\n4. Tester avec trailing slash..."
curl -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Bob",
    "last_name": "Smith", 
    "email": "bob_'$(date +%s)'@example.com",
    "password": "Password123"
  }'

echo -e "\n\n=== FIN TEST ==="