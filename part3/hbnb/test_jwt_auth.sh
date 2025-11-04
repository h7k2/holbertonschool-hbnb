#!/bin/bash

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://127.0.0.1:5000/api/v1"

# Générer un email unique avec timestamp
TIMESTAMP=$(date +%s)
USER_EMAIL="alice_${TIMESTAMP}@example.com"
ADMIN_EMAIL="admin_${TIMESTAMP}@example.com"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TEST COMPLET JWT AUTHENTICATION${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 1: Créer un utilisateur
echo -e "${YELLOW}Test 1: Créer un utilisateur (Alice)${NC}"
USER_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Alice\",
    \"last_name\": \"Johnson\",
    \"email\": \"$USER_EMAIL\",
    \"password\": \"password123\"
  }")
echo $USER_RESPONSE | python3 -m json.tool
USER_ID=$(echo $USER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ User ID: $USER_ID${NC}\n"

# Vérifier que l'utilisateur a bien été créé
if [ -z "$USER_ID" ]; then
    echo -e "${RED}✗ ERREUR: Utilisateur non créé!${NC}\n"
    exit 1
fi

# Test 2: Login et obtenir le token
echo -e "${YELLOW}Test 2: Login pour obtenir le JWT token${NC}"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$USER_EMAIL\",
    \"password\": \"password123\"
  }")
echo $LOGIN_RESPONSE | python3 -m json.tool
TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
echo -e "${GREEN}✓ Token obtenu: ${TOKEN:0:50}...${NC}\n"

# Test 3: Récupérer tous les utilisateurs (avec token)
echo -e "${YELLOW}Test 3: GET tous les utilisateurs (avec token)${NC}"
curl -s -X GET $BASE_URL/users/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "${GREEN}✓ Liste récupérée${NC}\n"

# Test 4: Récupérer un utilisateur spécifique (avec token)
echo -e "${YELLOW}Test 4: GET utilisateur spécifique (avec token)${NC}"
curl -s -X GET "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "${GREEN}✓ Utilisateur récupéré${NC}\n"

# Test 5: Mettre à jour l'utilisateur (avec token)
echo -e "${YELLOW}Test 5: PUT mise à jour de l'utilisateur (avec token)${NC}"
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alicia",
    "last_name": "Johnson-Smith"
  }' | python3 -m json.tool
echo -e "${GREEN}✓ Utilisateur mis à jour${NC}\n"

# Test 6: Endpoint protégé
echo -e "${YELLOW}Test 6: GET endpoint protégé (avec token)${NC}"
curl -s -X GET $BASE_URL/auth/protected \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "${GREEN}✓ Accès autorisé${NC}\n"

# Test 7: Accès sans token (doit échouer - 401)
echo -e "${YELLOW}Test 7: GET sans token (doit retourner 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/users/)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
echo $BODY | python3 -m json.tool
if [ "$HTTP_CODE" = "401" ]; then
    echo -e "${GREEN}✓ 401 Unauthorized - Correct${NC}\n"
else
    echo -e "${RED}✗ Erreur: Expected 401, got $HTTP_CODE${NC}\n"
fi

# Test 8: Token invalide (doit échouer - 401)
echo -e "${YELLOW}Test 8: GET avec token invalide (doit retourner 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/users/ \
  -H "Authorization: Bearer token_invalide_bidon")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
echo $BODY | python3 -m json.tool
if [ "$HTTP_CODE" = "401" ]; then
    echo -e "${GREEN}✓ 401 Unauthorized - Correct${NC}\n"
else
    echo -e "${RED}✗ Erreur: Expected 401, got $HTTP_CODE${NC}\n"
fi

# Test 9: Mauvais mot de passe (doit échouer - 401)
echo -e "${YELLOW}Test 9: Login avec mauvais mot de passe (doit retourner 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$USER_EMAIL\",
    \"password\": \"mauvais_mot_de_passe\"
  }")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
echo $BODY | python3 -m json.tool
if [ "$HTTP_CODE" = "401" ]; then
    echo -e "${GREEN}✓ 401 Unauthorized - Correct${NC}\n"
else
    echo -e "${RED}✗ Erreur: Expected 401, got $HTTP_CODE${NC}\n"
fi

# Test 10: Email déjà utilisé (doit échouer - 409)
echo -e "${YELLOW}Test 10: Créer utilisateur avec email existant (doit retourner 409)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Bob\",
    \"last_name\": \"Smith\",
    \"email\": \"$USER_EMAIL\",
    \"password\": \"password123\"
  }")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
echo $BODY | python3 -m json.tool
if [ "$HTTP_CODE" = "409" ]; then
    echo -e "${GREEN}✓ 409 Conflict - Correct${NC}\n"
else
    echo -e "${RED}✗ Erreur: Expected 409, got $HTTP_CODE${NC}\n"
fi

# Test 11: Supprimer sans être admin (doit échouer - 403)
echo -e "${YELLOW}Test 11: DELETE utilisateur sans être admin (doit retourner 403)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
if [ ! -z "$BODY" ]; then
    echo $BODY | python3 -m json.tool
fi
if [ "$HTTP_CODE" = "403" ]; then
    echo -e "${GREEN}✓ 403 Forbidden - Correct${NC}\n"
else
    echo -e "${RED}✗ Erreur: Expected 403, got $HTTP_CODE${NC}\n"
fi

# Test 12: Créer un admin et supprimer un utilisateur
echo -e "${YELLOW}Test 12a: Créer un utilisateur admin${NC}"
ADMIN_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Admin\",
    \"last_name\": \"User\",
    \"email\": \"$ADMIN_EMAIL\",
    \"password\": \"admin123\",
    \"is_admin\": true
  }")
echo $ADMIN_RESPONSE | python3 -m json.tool
ADMIN_ID=$(echo $ADMIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ Admin créé - ID: $ADMIN_ID${NC}\n"

echo -e "${YELLOW}Test 12b: Login admin${NC}"
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$ADMIN_EMAIL\",
    \"password\": \"admin123\"
  }")
echo $ADMIN_LOGIN | python3 -m json.tool
ADMIN_TOKEN=$(echo $ADMIN_LOGIN | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
echo -e "${GREEN}✓ Token admin obtenu: ${ADMIN_TOKEN:0:50}...${NC}\n"

# Vérifier que le token admin est bien extrait
if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}✗ ERREUR: Token admin non extrait!${NC}\n"
    exit 1
fi

echo -e "${YELLOW}Test 12c: DELETE utilisateur avec token admin (doit réussir - 204)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
if [ "$HTTP_CODE" = "204" ]; then
    echo -e "${GREEN}✓ 204 No Content - Utilisateur supprimé${NC}\n"
else
    if [ ! -z "$BODY" ]; then
        echo $BODY | python3 -m json.tool
    fi
    echo -e "${RED}✗ Erreur: Expected 204, got $HTTP_CODE${NC}\n"
fi

# Test 13: Vérifier que l'utilisateur est bien supprimé (doit retourner 404)
echo -e "${YELLOW}Test 13: Vérifier que l'utilisateur supprimé n'existe plus (404)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
echo $BODY | python3 -m json.tool
if [ "$HTTP_CODE" = "404" ]; then
    echo -e "${GREEN}✓ 404 Not Found - Correct${NC}\n"
else
    echo -e "${RED}✗ Erreur: Expected 404, got $HTTP_CODE${NC}\n"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TOUS LES TESTS SONT TERMINÉS${NC}"
echo -e "${BLUE}========================================${NC}"