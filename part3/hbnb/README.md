# HBnB – Part 2 (BL & API)

## But
Mettre en place l’app Flask + l’API (flask-restx), la logique métier (modèles) et une persistance **en mémoire** via une **Façade**. La BDD arrivera en Part 3.

## Structure
hbnb/
├── app/
│ ├── init.py
│ ├── api/
│ │ └── v1/ (users.py, places.py, reviews.py, amenities.py)
│ ├── models/ (user.py, place.py, review.py, amenity.py)
│ ├── services/ (facade.py, init.py -> facade)
│ └── persistence/ (repository.py)
├── run.py
├── config.py
├── requirements.txt
└── README.md

bash
Copier le code

## Installation
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
requirements.txt :

nginx
Copier le code
flask
flask-restx
Lancer
bash
Copier le code
python run.py
Healthcheck : http://127.0.0.1:5000/health

Swagger : http://127.0.0.1:5000/api/v1/

Notes
Repos en mémoire : InMemoryRepository

Façade : HBnBFacade (instance unique exposée dans app/services/__init__.py)

Endpoints à ajouter ensuite dans app/api/v1/*.py