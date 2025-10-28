#!/bin/bash

echo "🗑️  SUPPRESSION DES DELETE NON CONFORMES"
echo "========================================"
echo ""

# User API
if [ -f "app/api/v1/users.py" ] && grep -q "def delete" app/api/v1/users.py; then
    echo "📝 User API: Suppression de DELETE..."
    cp app/api/v1/users.py app/api/v1/users.py.backup
    
    # Supprimer la méthode delete avec Python pour être plus précis
    python3 << 'PYEOF'
import re
with open('app/api/v1/users.py', 'r') as f:
    content = f.read()
# Supprimer la méthode delete et ses décorateurs
content = re.sub(r'\n\s+@api\.response.*?delete.*?\n.*?def delete\(.*?\):.*?(?=\n\s{0,8}(@api|def|class|\Z))', '', content, flags=re.DOTALL)
with open('app/api/v1/users.py', 'w') as f:
    f.write(content)
PYEOF
    echo "   ✅ DELETE supprimé de users.py"
else
    echo "✅ User API: Pas de DELETE (déjà conforme)"
fi

# Place API
if [ -f "app/api/v1/places.py" ] && grep -q "def delete" app/api/v1/places.py; then
    echo "📝 Place API: Suppression de DELETE..."
    cp app/api/v1/places.py app/api/v1/places.py.backup
    
    python3 << 'PYEOF'
import re
with open('app/api/v1/places.py', 'r') as f:
    content = f.read()
content = re.sub(r'\n\s+@api\.response.*?delete.*?\n.*?def delete\(.*?\):.*?(?=\n\s{0,8}(@api|def|class|\Z))', '', content, flags=re.DOTALL)
with open('app/api/v1/places.py', 'w') as f:
    f.write(content)
PYEOF
    echo "   ✅ DELETE supprimé de places.py"
else
    echo "✅ Place API: Pas de DELETE (déjà conforme)"
fi

# Amenity API
if [ -f "app/api/v1/amenities.py" ] && grep -q "def delete" app/api/v1/amenities.py; then
    echo "📝 Amenity API: Suppression de DELETE..."
    cp app/api/v1/amenities.py app/api/v1/amenities.py.backup
    
    python3 << 'PYEOF'
import re
with open('app/api/v1/amenities.py', 'r') as f:
    content = f.read()
content = re.sub(r'\n\s+@api\.response.*?delete.*?\n.*?def delete\(.*?\):.*?(?=\n\s{0,8}(@api|def|class|\Z))', '', content, flags=re.DOTALL)
with open('app/api/v1/amenities.py', 'w') as f:
    f.write(content)
PYEOF
    echo "   ✅ DELETE supprimé de amenities.py"
else
    echo "✅ Amenity API: Pas de DELETE (déjà conforme)"
fi

# Facade
echo ""
echo "📝 Nettoyage de la Facade..."
if [ -f "app/services/facade.py" ]; then
    cp app/services/facade.py app/services/facade.py.backup
    
    python3 << 'PYEOF'
import re
with open('app/services/facade.py', 'r') as f:
    content = f.read()

# Supprimer delete_user
if 'def delete_user' in content:
    content = re.sub(r'\n\s+def delete_user\(.*?\):.*?(?=\n\s{0,8}def |\Z)', '', content, flags=re.DOTALL)
    print("   ✅ delete_user supprimée")

# Supprimer delete_place
if 'def delete_place' in content:
    content = re.sub(r'\n\s+def delete_place\(.*?\):.*?(?=\n\s{0,8}def |\Z)', '', content, flags=re.DOTALL)
    print("   ✅ delete_place supprimée")

# Supprimer delete_amenity
if 'def delete_amenity' in content:
    content = re.sub(r'\n\s+def delete_amenity\(.*?\):.*?(?=\n\s{0,8}def |\Z)', '', content, flags=re.DOTALL)
    print("   ✅ delete_amenity supprimée")

with open('app/services/facade.py', 'w') as f:
    f.write(content)
PYEOF
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 VÉRIFICATION FINALE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "❌ User (ne doit PAS avoir DELETE):"
if grep -q "def delete" app/api/v1/users.py 2>/dev/null; then
    echo "   ⚠️  DELETE encore présent!"
else
    echo "   ✅ Aucun DELETE"
fi

echo ""
echo "❌ Place (ne doit PAS avoir DELETE):"
if grep -q "def delete" app/api/v1/places.py 2>/dev/null; then
    echo "   ⚠️  DELETE encore présent!"
else
    echo "   ✅ Aucun DELETE"
fi

echo ""
echo "❌ Amenity (ne doit PAS avoir DELETE):"
if grep -q "def delete" app/api/v1/amenities.py 2>/dev/null; then
    echo "   ⚠️  DELETE encore présent!"
else
    echo "   ✅ Aucun DELETE"
fi

echo ""
echo "✅ Review (DOIT avoir DELETE) ⭐:"
if grep -q "def delete" app/api/v1/reviews.py 2>/dev/null; then
    echo "   ✅ DELETE présent (conforme)"
    grep -n "def delete" app/api/v1/reviews.py
else
    echo "   ⚠️  DELETE absent (devrait être présent!)"
fi

echo ""
echo "✅ Facade - delete_review (DOIT exister) ⭐:"
if grep -q "def delete_review" app/services/facade.py 2>/dev/null; then
    echo "   ✅ delete_review présente (conforme)"
else
    echo "   ⚠️  delete_review absente (devrait être présente!)"
fi

echo ""
echo "💾 Sauvegardes créées:"
ls -la *.backup app/api/v1/*.backup app/services/*.backup 2>/dev/null || echo "   Aucune sauvegarde (fichiers déjà conformes)"

echo ""
echo "🎯 Nettoyage terminé!"
echo ""
echo "Pour restaurer si nécessaire:"
echo "  mv app/api/v1/users.py.backup app/api/v1/users.py"
echo "  mv app/api/v1/places.py.backup app/api/v1/places.py"
echo "  mv app/api/v1/amenities.py.backup app/api/v1/amenities.py"
echo "  mv app/services/facade.py.backup app/services/facade.py"
