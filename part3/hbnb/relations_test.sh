#!/bin/bash

echo "=== TEST DES RELATIONS (URLs CORRIGÉES) ==="

# 1. Créer utilisateur
echo "1. Créer utilisateur..."
USER_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Alice\",
    \"last_name\": \"Johnson\", 
    \"email\": \"alice_$(date +%s)@test.com\",
    \"password\": \"password123\"
  }")

echo "$USER_RESPONSE" | python3 -m json.tool
USER_ID=$(echo "$USER_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "User ID: $USER_ID"

if [ -z "$USER_ID" ]; then
    echo "❌ Impossible de créer l'utilisateur"
    exit 1
fi

# 2. Se connecter
echo -e "\n2. Se connecter..."
# CORRECTION - Utiliser le bon email
EMAIL=$(echo "$USER_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('email', ''))" 2>/dev/null)

LOGIN_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"password123\"
  }")

echo "$LOGIN_RESPONSE" | python3 -m json.tool
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('access_token', ''))" 2>/dev/null)
echo "Token: ${TOKEN:0:50}..."

if [ -z "$TOKEN" ]; then
    echo "❌ Impossible de récupérer le token"
    exit 1
fi

# 3. Créer place
echo -e "\n3. Créer place..."
PLACE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Appartement Test",
    "description": "Test des relations",
    "price": 75.0,
    "latitude": 48.8566,
    "longitude": 2.3522
  }')

echo "$PLACE_RESPONSE" | python3 -m json.tool
PLACE_ID=$(echo "$PLACE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "Place ID: $PLACE_ID"

if [ -z "$PLACE_ID" ]; then
    echo "❌ Impossible de créer une place"
    echo "Debug - Response: $PLACE_RESPONSE"
    exit 1
fi

echo "✅ Place créée avec succès !"

# 4. Créer amenity
echo -e "\n4. Créer amenity..."
AMENITY_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')

echo "$AMENITY_RESPONSE" | python3 -m json.tool
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "Amenity ID: $AMENITY_ID"

# 5. Tester les relations AVEC le token
if [ ! -z "$PLACE_ID" ] && [ ! -z "$USER_ID" ] && [ ! -z "$TOKEN" ]; then
    echo -e "\n5. Tester les relations..."
    
    # Test: Places de l'utilisateur AVEC token
    echo "- Places de l'utilisateur:"
    curl -s -H "Authorization: Bearer $TOKEN" "http://127.0.0.1:5000/api/v1/users/$USER_ID/places/" | python3 -m json.tool
    
    # Test: Reviews de la place (pas besoin de token)
    echo -e "\n- Reviews de la place:"
    curl -s "http://127.0.0.1:5000/api/v1/places/$PLACE_ID/reviews/" | python3 -m json.tool
    
    # Test: Amenities de la place (pas besoin de token)
    echo -e "\n- Amenities de la place:"
    curl -s "http://127.0.0.1:5000/api/v1/places/$PLACE_ID/amenities/" | python3 -m json.tool
    
    # Test: Ajouter amenity à la place (avec token)
    if [ ! -z "$AMENITY_ID" ]; then
        echo -e "\n- Ajouter amenity à la place:"
        curl -s -X POST "http://127.0.0.1:5000/api/v1/places/$PLACE_ID/amenities/" \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $TOKEN" \
          -d "{\"amenity_id\": \"$AMENITY_ID\"}" | python3 -m json.tool
        
        # Vérifier les amenities de la place après ajout
        echo -e "\n- Amenities de la place après ajout:"
        curl -s "http://127.0.0.1:5000/api/v1/places/$PLACE_ID/amenities/" | python3 -m json.tool
    fi
fi

echo -e "\n=== FIN TEST ==="