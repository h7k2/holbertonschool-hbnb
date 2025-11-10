![HBnB - Auth & DB Banner](image/HBnB%20-%20Auth%20&%20DB.jpg)

🏠 HBnB – Part 3: Authentication & Database Integration

Welcome to Part 3 of HBnB. In this stage, we move from an in-memory prototype to a secure and persistent backend using Flask, JWT, and SQLAlchemy. We add user authentication, authorization (RBAC), and database integration (SQLite in development, MySQL in production).

## 🎯 Objectives

- JWT authentication with `flask-jwt-extended`
- Role-based access control using the `is_admin` attribute
- Replace in-memory storage with a database (SQLite for development, prepare MySQL for production)
- Full persistence for entities: User, Place, Review, Amenity
- Data validation and constraints enforcement

## 🧠 Learning goals

- Implement JWT authentication and manage sessions at the API level
- Apply RBAC (role-based access control)
- Use SQLAlchemy for ORM mapping, queries, and relationships
- Configure SQLite (dev) and prepare MySQL (prod)
- Visualize the relational schema (Mermaid.js) and document the architecture

## 🧱 Project structure

```
part3/
	hbnb/
		app/
			__init__.py        # Application Factory
			extensions.py       # (if present) Flask/JWT/DB extensions
			api/                # Flask-RestX namespaces & routes
			models/             # SQLAlchemy models (User, Place, Review, Amenity, Base)
			persistence/        # SQLAlchemy repositories
			services/           # Business logic & Facade
		run.py                # Flask app entry point
		config.py             # Dev/Prod configurations
		requirements.txt      # Dependencies
	instance/
		hbnb.sqlite3          # SQLite database (dev)
	README.md               # Documentation (this file)
```

## ⚙️ Prerequisites & Setup (Linux/Bash)

1) Clone the repo and go to `part3/hbnb`
2) Create a Python 3.10+ virtual environment
3) Install dependencies from `hbnb/requirements.txt`
4) Run the app with `hbnb/run.py`

The app starts by default at: http://127.0.0.1:5000/

Tip: `hbnb/config.py` controls the configuration (development/production) used by the Application Factory.

## 🔐 Authentication & Roles

- Sign up: `POST /api/v1/users/` (password hashed with bcrypt, never returned in responses)
- Login: `POST /api/v1/login/` (returns a JWT)
- Protected access: add the header `Authorization: Bearer <token>`
- RBAC: admin-only endpoints require `is_admin = True`

## 🧩 Endpoints (examples)

- Public
	- `POST /api/v1/users/` — create a user (sign up)
	- `POST /api/v1/login/` — authenticate (JWT)
	- `GET /api/v1/places/` — list places

- Authenticated
	- `POST /api/v1/places/` — create a place (owner = current user)
	- `PUT /api/v1/users/<id>` — update own profile (except email/password)
	- `DELETE /api/v1/places/<id>` — delete a place (owner or admin)
	- `POST /api/v1/reviews/` — create a review (not on your own place, no duplicates)

- Administrator
	- Create/update any user (including email/password)
	- Add/update amenities
	- Bypass ownership restrictions (places/reviews)

## 🧰 Technologies

- Python 3.10+
- Flask 3.x, Flask-RESTX
- Flask-JWT-Extended, Flask-Bcrypt, Flask-SQLAlchemy
- SQLite (dev) / MySQL (prod)
- Mermaid.js (ER diagrams)

## 📚 Task plan (Part 3)

0) Application Factory & Configuration
- Update `create_app()` to accept a config object and initialize extensions.

1) Password hashing (bcrypt)
- Secure password storage; field accepted in POST /users/; never returned by GET.

2) JWT authentication
- Login, token generation/validation, claims like `is_admin` for authorization.

3) Authenticated user access
- Secure create/update/delete (places, reviews) with ownership checks and business rules.

4) Administrator access
- Admin-only endpoints: create/update users, amenities, bypass ownership restrictions.

5) SQLAlchemy repository
- Replace the in-memory repository with a SQLAlchemy-based implementation.

6) User model mapping
- Map `Base`/`BaseModel` + `User` (first_name, last_name, unique email, hashed password, is_admin) and implement `UserRepository`.

7) Place, Review, Amenity mapping
- Map basic attributes and CRUD, without relationships yet.

8) Relationships between entities
- Define FKs and relationships (One-to-Many, Many-to-Many) among User, Place, Review, Amenity.

9) SQL scripts
- Generate the full schema and insert seed data (admin, amenities) for testing.

10) ER diagrams
- Produce an ERD with Mermaid.js and include it in the documentation.

## 🗺️ Database diagram

![ER Diagram](../image/diagramme.png)

The diagram above shows the main entities (User, Place, Review, Amenity) and their relationships (e.g., a User owns many Places, a Place has many Reviews, Place ↔ Amenity is many-to-many).

## 🧪 Quick checks (examples)

- Sign up a user, then log in to get a JWT.
- Call a protected endpoint with `Authorization: Bearer <token>`.
- Verify that:
	- you cannot create/update/delete resources without a JWT,
	- a user can only modify their own data (except admins),
	- business rules are enforced (no reviews on your own place, no duplicates).

## 🙌 Team

- Heytem Keddous (h7k2)
- Zaccaria Azladji
- (Team project — Holberton School)

## 📄 License

Academic project within the Holberton School curriculum. Please follow the collaboration rules and license associated with the Project.
