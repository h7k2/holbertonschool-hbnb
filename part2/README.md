🏠 HBnB – Part 2: Business Logic and API Endpoints

📖 Introduction

This part of the HBnB Evolution project marks the transition from design (Part 1) to implementation.
Here, you will bring your documented architecture to life by developing the Business Logic Layer and the Presentation Layer (API) using Python, Flask, and flask-restx.

The goal is to implement the core functionality of the application: creating, reading, updating, and managing the main entities — Users, Places, Amenities, and Reviews — while following the principles of clean architecture and RESTful API design.

⚠️ Note: JWT authentication and role-based access control will be implemented in Part 3.
In this parZEt, data is stored in an in-memory repository, which will later be replaced by a database.

🎯 Objectives

By the end of this project, you will be able to:

🧩 1. Project Setup

Structure a Python application following modular architecture best practices.

Create separate packages for:

Presentation Layer (Flask API)

Business Logic Layer (Core entities and logic)

Persistence Layer (In-memory repository, prepared for future SQLAlchemy integration)

Prepare the Facade Pattern for communication between layers.

⚙️ 2. Business Logic Layer

Implement core classes and relationships:

User, Place, Review, and Amenity

Manage entity relationships (e.g., a User owns multiple Places).

Validate attributes (e.g., required fields, data types).

Provide methods for creation, update, and relationship management.

🌐 3. RESTful API Endpoints

Build a Flask + flask-restx API exposing CRUD operations:

POST, GET, PUT (no DELETE yet for users, places, amenities)

Full CRUD for Review

Return JSON responses with proper status codes and validation errors.

Serialize data, including nested/related fields (e.g., owner details inside a Place).

🧪 4. Testing and Validation

Test endpoints using cURL or Postman.

Validate input/output formats.

Generate Swagger documentation automatically from flask-restx.

Write unit tests using unittest or pytest.

🏗️ Project Structure
holbertonschool-hbnb/
│
├── part2/
│   ├── app.py                       # Flask entry point
│   │
│   ├── presentation/                # Presentation Layer (API)
│   │   ├── __init__.py
│   │   ├── api_namespace.py
│   │   ├── users_endpoints.py
│   │   ├── places_endpoints.py
│   │   ├── reviews_endpoints.py
│   │   ├── amenities_endpoints.py
│   │
│   ├── business_logic/              # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │
│   ├── persistence/                 # Persistence Layer (In-memory)
│   │   ├── __init__.py
│   │   ├── repository.py
│   │
│   ├── facade/                      # Facade pattern connector
│   │   ├── __init__.py
│   │   ├── hbnb_facade.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_users.py
│       ├── test_places.py
│       ├── test_reviews.py
│       └── test_amenities.py
│
└── README.md

🧱 Tasks Overview
Task 0 – Project Setup and Package Initialization

Create the folder structure for presentation/, business_logic/, and persistence/.

Implement an in-memory repository to temporarily store data.

Prepare the Facade pattern for communication between layers.

Task 1 – Core Business Logic Classes

Implement:

User

Place

Review

Amenity

Include validation (UUIDs, timestamps, etc.)

Define relationships (e.g., one user → many places).

Task 2 – User Endpoints

Implement CRUD operations (except DELETE):

POST /api/v1/users

GET /api/v1/users/<id>

GET /api/v1/users

PUT /api/v1/users/<id>

Passwords must not appear in responses.

Task 3 – Amenity Endpoints

Implement CRUD (except DELETE):

POST /api/v1/amenities

GET /api/v1/amenities/<id>

PUT /api/v1/amenities/<id>

Task 4 – Place Endpoints

Implement CRUD (except DELETE):

POST /api/v1/places

GET /api/v1/places/<id>

PUT /api/v1/places/<id>

Handle relationships (User as owner, amenities linked).

Validate price, latitude, longitude.

Task 5 – Review Endpoints

Implement full CRUD:

POST /api/v1/reviews

GET /api/v1/reviews/<id>

PUT /api/v1/reviews/<id>

DELETE /api/v1/reviews/<id>

Link each review to both a user and a place.

Task 6 – Testing and Validation

Validate all inputs (types, required fields).

Test endpoints using cURL and Swagger.

Create automated tests with unittest or pytest.

Document test results and edge cases.

🔗 Example API Endpoints
Method	Endpoint	Description
POST	/api/v1/users	Create a new user
GET	/api/v1/users/<id>	Retrieve a user by ID
GET	/api/v1/places	List all places
PUT	/api/v1/places/<id>	Update a place
DELETE	/api/v1/reviews/<id>	Delete a review
GET	/api/v1/amenities	List all amenities
🧠 Key Concepts Used

Flask – micro web framework for Python

flask-restx – structured REST API and documentation

In-Memory Repository – temporary storage system

Facade Pattern – interface simplifying layer communication

Serialization – converting Python objects into JSON

OOP Principles – encapsulation, inheritance, composition

Separation of Concerns – modular and maintainable design

🧰 Tools & Resources

Flask Documentation

flask-restx Documentation

Python Project Structure Best Practices

REST API Design Best Practices

Facade Design Pattern in Python

🧪 Testing Example (cURL)
# Create a user
curl -X POST http://127.0.0.1:5000/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Alice", "last_name": "Doe", "email": "alice@example.com"}'

# Get list of users
curl -X GET http://127.0.0.1:5000/api/v1/users

👥 Team

Heytem Keddous

Zaccaria Azladji

[Add third teammate name here]

Project developed as part of the Holberton School HBnB Evolution project – Part 2.

🧾 License

This project is part of the Holberton School Curriculum.
All rights reserved © 2025 – HBnB Evolution Team.