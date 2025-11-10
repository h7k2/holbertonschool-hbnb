#!/bin/bash

echo "🚀 CRÉATION D'UN SCÉNARIO COMPLET AVEC RELATIONS"

BASE_URL="http://127.0.0.1:5000/api/v1"

# 1. Créer un utilisateur
echo "👤 1. Création utilisateur..."
USER_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Dupont", 
    "email": "alice.dupont@example.com",
    "password": "password123"
  }')

echo "$USER_RESPONSE" | python3 -m json.tool
USER_ID=$(echo "$USER_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "✅ User ID: $USER_ID"

# 2. Se connecter pour obtenir le token
echo -e "\n🔐 2. Connexion..."
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.dupont@example.com",
    "password": "password123"
  }')

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('access_token', ''))" 2>/dev/null)
echo "✅ Token obtenu: ${TOKEN:0:50}..."

# 3. Créer une place pour cet utilisateur
echo -e "\n🏠 3. Création place..."
PLACE_RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Appartement Cosy à Paris",
    "description": "Bel appartement 2 pièces au cœur de Paris, proche métro",
    "price": 85.0,
    "latitude": 48.8566,
    "longitude": 2.3522
  }')

echo "$PLACE_RESPONSE" | python3 -m json.tool
PLACE_ID=$(echo "$PLACE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "✅ Place ID: $PLACE_ID"

# 4. Créer plusieurs amenities
echo -e "\n🌟 4. Création amenities..."

# WiFi
WIFI_RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi Gratuit"}')
WIFI_ID=$(echo "$WIFI_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "✅ Wi-Fi ID: $WIFI_ID"

# Parking
PARKING_RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Parking Privé"}')
PARKING_ID=$(echo "$PARKING_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "✅ Parking ID: $PARKING_ID"

# Cuisine
CUISINE_RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Cuisine Équipée"}')
CUISINE_ID=$(echo "$CUISINE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
echo "✅ Cuisine ID: $CUISINE_ID"

# 5. Associer les amenities à la place
echo -e "\n🔗 5. Association amenities → place..."

curl -s -X POST "$BASE_URL/places/$PLACE_ID/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"amenity_id\": \"$WIFI_ID\"}" | python3 -m json.tool

curl -s -X POST "$BASE_URL/places/$PLACE_ID/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"amenity_id\": \"$PARKING_ID\"}" | python3 -m json.tool

curl -s -X POST "$BASE_URL/places/$PLACE_ID/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"amenity_id\": \"$CUISINE_ID\"}" | python3 -m json.tool

# 6. Créer une review
echo -e "\n⭐ 6. Création review..."
REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/places/$PLACE_ID/reviews/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Excellent appartement ! Très bien situé et bien équipé. Je recommande vivement !",
    "rating": 5
  }')

echo "$REVIEW_RESPONSE" | python3 -m json.tool

# 7. Vérifications finales
echo -e "\n📊 7. VÉRIFICATIONS FINALES:"

echo "- Places de l'utilisateur:"
curl -s "$BASE_URL/users/$USER_ID/places/" | python3 -m json.tool

echo -e "\n- Amenities de la place:"
curl -s "$BASE_URL/places/$PLACE_ID/amenities/" | python3 -m json.tool

echo -e "\n- Reviews de la place:"
curl -s "$BASE_URL/places/$PLACE_ID/reviews/" | python3 -m json.tool

echo -e "\n🎉 SCÉNARIO COMPLET CRÉÉ AVEC SUCCÈS!"
echo "User: Alice Dupont"
echo "Place: Appartement Cosy à Paris"  
echo "Amenities: Wi-Fi, Parking, Cuisine"
echo "Review: 5 étoiles"
