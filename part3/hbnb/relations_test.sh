#!/bin/bash

API_BASE="http://127.0.0.1:5000/api/v1"
EMAIL="alice_$(date +%s)@test.com"

echo "=== TEST DES RELATIONS (URLs CORRIGÉES) ==="

echo "1. Créer utilisateur..."
USER_RESPONSE=$(curl -s -X POST $API_BASE/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Johnson", 
    "email": "'$EMAIL'",
    "password": "Password123"
  }')

echo "$USER_RESPONSE"
USER_ID=$(echo "$USER_RESPONSE" | sed -n 's/.*"id": *"\([^"]*\)".*/\1/p')
echo "User ID: $USER_ID"

if [ -n "$USER_ID" ] && [ "$USER_ID" != "" ]; then
    echo -e "\n2. Se connecter..."
    LOGIN_RESPONSE=$(curl -s -X POST $API_BASE/auth/login \
      -H "Content-Type: application/json" \
      -d '{
        "email": "'$EMAIL'",
        "password": "Password123"
      }')

    echo "$LOGIN_RESPONSE"
    TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/.*"access_token": *"\([^"]*\)".*/\1/p')
    echo "Token: ${TOKEN:0:30}..."

    if [ -n "$TOKEN" ] && [ "$TOKEN" != "" ]; then
        echo -e "\n3. Créer place..."
        PLACE_RESPONSE=$(curl -s -X POST $API_BASE/places/ \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $TOKEN" \
          -d '{
            "name": "Appartement Test",
            "description": "Test des relations",
            "price_by_night": 75,
            "latitude": 48.8566,
            "longitude": 2.3522
          }')

        echo "$PLACE_RESPONSE"
        PLACE_ID=$(echo "$PLACE_RESPONSE" | sed -n 's/.*"id": *"\([^"]*\)".*/\1/p')
        echo "Place ID: $PLACE_ID"

        if [ -n "$PLACE_ID" ] && [ "$PLACE_ID" != "" ]; then
            echo -e "\n4. Créer amenity..."
            AMENITY_RESPONSE=$(curl -s -X POST $API_BASE/amenities/ \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer $TOKEN" \
              -d '{
                "name": "Wi-Fi Gratuit"
              }')

            echo "$AMENITY_RESPONSE"
            AMENITY_ID=$(echo "$AMENITY_RESPONSE" | sed -n 's/.*"id": *"\([^"]*\)".*/\1/p')
            echo "Amenity ID: $AMENITY_ID"

            echo -e "\n5. Créer review..."
            REVIEW_RESPONSE=$(curl -s -X POST $API_BASE/reviews/ \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer $TOKEN" \
              -d '{
                "place_id": "'$PLACE_ID'",
                "text": "Excellent appartement, très propre!",
                "rating": 5
              }')

            echo "$REVIEW_RESPONSE"
            REVIEW_ID=$(echo "$REVIEW_RESPONSE" | sed -n 's/.*"id": *"\([^"]*\)".*/\1/p')
            echo "Review ID: $REVIEW_ID"

            echo -e "\n=== TESTS DES RELATIONS ==="

            echo -e "\n6. User -> Places (One-to-Many)"
            echo "Tentative: GET /users/$USER_ID/places/"
            USER_PLACES_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_BASE/users/$USER_ID/places/")
            echo "$USER_PLACES_RESPONSE"
            
            if [[ "$USER_PLACES_RESPONSE" == *"404"* ]] || [[ "$USER_PLACES_RESPONSE" == *"Not Found"* ]]; then
                echo "Tentative alternative: GET /users/me/places/"
                curl -s -H "Authorization: Bearer $TOKEN" "$API_BASE/users/me/places/"
            fi

            echo -e "\n\n7. Place -> Reviews (One-to-Many)"
            echo "GET /places/$PLACE_ID/reviews/"
            curl -s "$API_BASE/places/$PLACE_ID/reviews/"

            echo -e "\n\n8. User -> Reviews (One-to-Many)"  
            echo "Tentative: GET /users/$USER_ID/reviews/"
            USER_REVIEWS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_BASE/users/$USER_ID/reviews/")
            echo "$USER_REVIEWS_RESPONSE"
            
            if [[ "$USER_REVIEWS_RESPONSE" == *"404"* ]] || [[ "$USER_REVIEWS_RESPONSE" == *"Not Found"* ]]; then
                echo "Tentative alternative: GET /users/me/reviews/"
                curl -s -H "Authorization: Bearer $TOKEN" "$API_BASE/users/me/reviews/"
            fi

            if [ -n "$AMENITY_ID" ] && [ "$AMENITY_ID" != "" ]; then
                echo -e "\n\n9. Place <-> Amenity (Many-to-Many) - Liaison"
                echo "POST /places/$PLACE_ID/amenities/"
                LINK_RESPONSE=$(curl -s -X POST "$API_BASE/places/$PLACE_ID/amenities/" \
                  -H "Content-Type: application/json" \
                  -H "Authorization: Bearer $TOKEN" \
                  -d '{"amenity_id": "'$AMENITY_ID'"}')
                echo "$LINK_RESPONSE"

                echo -e "\n\n10. Vérifier amenities de la place"
                echo "GET /places/$PLACE_ID/amenities/"
                curl -s "$API_BASE/places/$PLACE_ID/amenities/"

                echo -e "\n\n11. Vérifier places de l'amenity (si disponible)"
                echo "GET /amenities/$AMENITY_ID/places/"
                curl -s "$API_BASE/amenities/$AMENITY_ID/places/"
            fi
        else
            echo "❌ Impossible de créer une place"
        fi
    else
        echo "❌ Impossible de se connecter"
    fi
else
    echo "❌ Impossible de créer l'utilisateur"
fi

echo -e "\n\n=== FIN TEST ==="