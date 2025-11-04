

🏠 HBnB – Part 3: Authentication & Database Integration
📘 Project Overview

HBnB – Part 3 marks the transition of the HBnB application from a simple in-memory prototype to a secure and persistent backend powered by Flask, JWT authentication, and SQLAlchemy ORM.
This stage introduces user authentication, authorization, and database integration to prepare the system for real-world deployment.

🚀 Objectives
🔐 Authentication & Authorization

Implement JWT-based authentication using flask-jwt-extended.

Introduce role-based access control (RBAC) using an is_admin attribute.

Protect private routes and allow only authenticated users or admins to access them.

🗃️ Database Integration

Replace the in-memory storage with SQLite for development.

Prepare configuration for MySQL in production.

Use SQLAlchemy to map entities and manage database persistence.

⚙️ CRUD Operations & Persistence

Refactor all CRUD endpoints to interact with the database.

Ensure that all entities — User, Place, Review, and Amenity — are stored persistently.

🧩 Data Modeling & Validation

Design the relational schema using Mermaid.js.

Enforce validation and integrity rules for all data models.

🧠 Learning Objectives

By the end of this project, you will be able to:

Implement secure JWT authentication and manage user sessions.

Apply role-based authorization to protect API endpoints.

Use SQLAlchemy ORM for model mapping, queries, and relationships.

Integrate SQLite for development and configure MySQL for production.

Design and visualize ER diagrams with Mermaid.js.

Build a scalable, secure, and persistent backend architecture.

🧱 Project Structure
part3/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Config classes (Development, Production)
│   ├── models/              # SQLAlchemy models (User, Place, Review, Amenity)
│   ├── repository/          # SQLAlchemyRepository implementation
│   ├── services/            # Business logic & Facade layer
│   ├── api/                 # Flask-RestX namespaces & routes
│   └── utils/               # JWT, auth decorators, and helpers
│
├── instance/
│   └── hbnb.sqlite3         # SQLite database (dev)
│
├── run.py                   # Entry point for Flask app
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
└── er_diagram.mmd           # Mermaid.js Entity Relationship Diagram

🧩 Key Tasks
#	Task	Description
0	Modify Application Factory	Add configuration support to create_app()
1	Password Hashing	Securely store passwords with bcrypt
2	JWT Authentication	Implement login & token-based protection
3	Authenticated User Endpoints	Restrict actions to logged-in users
4	Admin Endpoints	Role-based access for administrators
5	SQLAlchemy Repository	Replace in-memory repo with DB-based repo
6	Map User Entity	Define User model and integrate CRUD operations
7	Map Place, Review, Amenity	Map additional entities to the DB
8	Relationships	Add foreign keys and entity relationships
9	SQL Scripts	Generate tables and populate with initial data
10	ER Diagram	Create a visual Mermaid.js database schema
🧰 Technologies Used

Python 3.10+

Flask 3.x

Flask-JWT-Extended

Flask-Bcrypt

Flask-SQLAlchemy

SQLite / MySQL

Mermaid.js (for ER diagrams)

RESTful API architecture

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3

2️⃣ Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Flask app
python3 run.py


The app will start on:

http://127.0.0.1:5000/

🔐 Authentication Workflow

User Registration → POST /api/v1/users/

Creates a new user and stores a hashed password.

User Login → POST /api/v1/login/

Returns a JWT token.

Protected Routes

Must include Authorization: Bearer <token> header.

Role-based Access

Admin endpoints restricted to users with is_admin = True.

🧮 Example API Endpoints
Method	Endpoint	Description	Auth Required
POST	/api/v1/users/	Register new user	❌
POST	/api/v1/login/	Authenticate and get JWT	❌
GET	/api/v1/places/	List all places	❌
POST	/api/v1/places/	Create new place	✅
PUT	/api/v1/users/<id>	Update user info	✅
DELETE	/api/v1/places/<id>	Delete place (owner/admin)	✅
GET	/api/v1/amenities/	List all amenities	❌
POST	/api/v1/amenities/	Add amenity (admin only)	🔒
🗺️ Database Schema (Mermaid.js)
erDiagram
    USER {
        UUID id PK
        STRING first_name
        STRING last_name
        STRING email UNIQUE
        STRING password
        BOOLEAN is_admin
    }

    PLACE {
        UUID id PK
        STRING name
        TEXT description
        FLOAT price
        UUID user_id FK
    }

    REVIEW {
        UUID id PK
        TEXT comment
        INT rating
        UUID user_id FK
        UUID place_id FK
    }

    AMENITY {
        UUID id PK
        STRING name
    }

    PLACE ||--o{ REVIEW : has
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE }o--o{ AMENITY : features

👥 Team Members

Heytem Keddous

Zaccaria Azladji


🧾 License

This project is part of the Holberton School curriculum and follows its academic license and collaboration rules.
