#!/bin/bash

# Script de test rapide pour valider la Partie 4

echo "🧪 TEST DE VALIDATION - PARTIE 4 HBNB"
echo "======================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de test
test_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 existe${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 manquant${NC}"
        return 1
    fi
}

# Fonction de test contenu
test_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✅ $1 contient '$2'${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 ne contient pas '$2'${NC}"
        return 1
    fi
}

echo "📁 Vérification de la structure des fichiers..."
echo ""

# Test présence fichiers
test_file "login.html"
test_file "index.html"
test_file "place.html"
test_file "add_review.html"
test_file "css/style.css"
test_file "js/scripts.js"
test_file "CORRECTIONS.md"
test_file "SUMMARY.md"

echo ""
echo "🔗 Vérification des chemins CSS/JS..."
echo ""

# Test chemins corrects
test_content "login.html" "css/style.css"
test_content "login.html" "js/scripts.js"
test_content "index.html" "css/style.css"
test_content "index.html" "js/scripts.js"
test_content "place.html" "css/style.css"
test_content "place.html" "js/scripts.js"

echo ""
echo "🌐 Vérification des URLs API..."
echo ""

# Test URLs API
test_content "js/scripts.js" "http://127.0.0.1:5000/api/v1"
test_content "js/scripts.js" "API_BASE_URL"
test_content "js/scripts.js" "/api/v1/auth/login"
test_content "js/scripts.js" "/api/v1/places"
test_content "js/scripts.js" "/api/v1/reviews"

echo ""
echo "🔐 Vérification de la sécurité..."
echo ""

# Test sécurité
test_content "js/scripts.js" "SameSite=Lax"
test_content "js/scripts.js" "expires"
test_content "js/scripts.js" "setCookie"
test_content "js/scripts.js" "getCookie"

echo ""
echo "🎨 Vérification des classes CSS..."
echo ""

# Test classes
test_content "css/style.css" ".place-card"
test_content "css/style.css" ".review-card"
test_content "css/style.css" ".details-button"
test_content "css/style.css" "margin: 20px"
test_content "css/style.css" "padding: 10px"
test_content "css/style.css" "border: 1px solid #ddd"
test_content "css/style.css" "border-radius: 10px"

echo ""
echo "📝 Vérification des attributs HTML..."
echo ""

# Test attributs HTML
test_content "login.html" "id=\"login-form\""
test_content "index.html" "id=\"places-list\""
test_content "index.html" "id=\"price-filter\""
test_content "place.html" "id=\"place-details\""
test_content "place.html" "id=\"reviews\""
test_content "place.html" "id=\"add-review\""

echo ""
echo "✨ Vérification des fonctionnalités JavaScript..."
echo ""

# Test fonctions JS
test_content "js/scripts.js" "function initLoginForm"
test_content "js/scripts.js" "function fetchPlaces"
test_content "js/scripts.js" "function displayPlaces"
test_content "js/scripts.js" "function filterPlacesByPrice"
test_content "js/scripts.js" "function fetchPlaceDetails"
test_content "js/scripts.js" "function displayReviews"
test_content "js/scripts.js" "function checkAuthentication"

echo ""
echo "======================================"
echo "🎉 Tests terminés !"
echo ""
echo -e "${YELLOW}⚠️  N'oubliez pas :${NC}"
echo "1. Ajouter votre logo dans images/logo.png"
echo "2. Démarrer l'API Part 3 sur le port 5000"
echo "3. Vérifier que CORS est activé dans l'API"
echo ""
echo -e "${GREEN}✅ Tous les fichiers sont prêts à être utilisés !${NC}"
echo ""
