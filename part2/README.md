# HBNB - Holberton BnB

## Project Overview
RESTful API for a Bed and Breakfast service built with Flask, implementing clean architecture patterns.

## 📁 Project Structure
```bash
part2/
├── app/
│   ├── api/v1/          # API endpoints
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── amenities.py
│   ├── models/          # Business logic
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/        # Facade pattern
│   └── persistence/     # Repository pattern
├── run.py               # Application entry point
└── requirements.txt     # Project dependencies
````

## Installation & Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🧩 Core Components

### 1. Base Model

```python
class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
```

### 2. Core Models

* **User**

  * Attributes: `first_name`, `last_name`, `email`, `is_admin`
  * Validation: names ≤ 50 chars, unique email

* **Place**

  * Attributes: `title`, `description`, `price`, `latitude`, `longitude`
  * Validation: title ≤ 100 chars, price > 0
  * Relationships: belongs to `User`, has many `Reviews`, many `Amenities`

* **Review**

  * Attributes: `text`, `rating (1-5)`, `user_id`, `place_id`
  * Relationships: belongs to `User` and `Place`

* **Amenity**

  * Attributes: `name (≤ 50 chars)`
  * Relationships: many-to-many with `Place`

### 3. Facade Pattern

```python
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Example methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_place_with_details(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            place.owner = self.user_repo.get(place.owner_id)
            place.reviews = self.review_repo.get_by_place(place_id)
        return place
```

## 🔌 API Endpoints & Examples

### User Management

```bash
# Create User
POST /api/v1/users/
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}

# Response
{
    "id": "uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}
```

### Place Management

```bash
# Create Place
POST /api/v1/places/
{
    "title": "Cozy Apartment",
    "description": "Nice stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "user_uuid",
    "amenities": ["amenity_uuid"]
}

# Get Place Details
GET /api/v1/places/<place_id>
Response includes: owner details, amenities, reviews
```

### Review Management

```bash
# Create Review
POST /api/v1/reviews/
{
    "text": "Great place!",
    "rating": 5,
    "user_id": "user_uuid",
    "place_id": "place_uuid"
}

# Get Place Reviews
GET /api/v1/places/<place_id>/reviews
```

### Amenity Management

```bash
# Create Amenity
POST /api/v1/amenities/
{
    "name": "Wi-Fi"
}

# Get All Amenities
GET /api/v1/amenities/
```

## 📊 Status Codes & Responses

* 201: Resource Created
* 200: Success
* 404: Not Found
* 400: Bad Request
* 500: Problem on Database

### 📝 Common Response Format

```json
{
    "id": "uuid",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    ...resource specific fields...
}
```

## 🏃‍♂️ Running the Application

```bash
python run.py  # Server starts at http://localhost:5000
```

---

## **Summary**: The project implements a REST API for a BnB platform by use Flask, clean architecture with Facade and Repository, managing users, places, reviews, and amenities through a structured endpoint system.



# HBNB API - Test Report

---

## ✅ Test Results Summary

| Endpoint | Method | Test Case | Status | Result |
|----------|--------|-----------|--------|--------|
| `/api/v1/users/` | POST | Create valid user | 201 | ✅ PASS |
| `/api/v1/users/` | GET | Get all users | 200 | ✅ PASS |
| `/api/v1/amenities/` | POST | Create amenity | 201 | ✅ PASS |
| `/api/v1/amenities/` | GET | Get all amenities | 200 | ✅ PASS |
| `/api/v1/places/` | POST | Create place | 201 | ✅ PASS |
| `/api/v1/places/` | GET | Get all places | 200 | ✅ PASS |
| `/api/v1/reviews/` | POST | Create review | 201 | ✅ PASS |
| `/api/v1/reviews/` | GET | Get all reviews | 200 | ✅ PASS |


---

## 📝 Detailed Test Cases

### 1. User Endpoints

#### ✅ Test 1.1: Create Valid User
**Request**:
```bash
POST /api/v1/users/
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com"
}
```

**Response**: `201 Created`
```json
{
    "id": "3b5adcc3-587b-48d7-bf4b-78747c2b3855",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com"
}
```

#### ✅ Test 1.2: Invalid Email Format
**Request**:
```bash
POST /api/v1/users/
Content-Type: application/json

{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "invalid"
}
```

**Response**: `400 Bad Request`
```json
{
    "error": "Invalid email format"
}
```

#### ✅ Test 1.3: Get All Users
**Request**: `GET /api/v1/users/`

**Response**: `200 OK`
```json
[
    {
        "id": "3b5adcc3-587b-48d7-bf4b-78747c2b3855",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com"
    }
]
```

---

### 2. Amenity Endpoints

#### ✅ Test 2.1: Create Amenity
**Request**:
```bash
POST /api/v1/amenities/
Content-Type: application/json

{
    "name": "WiFi"
}
```

**Response**: `201 Created`
```json
{
    "id": "390f1206-bf37-4b8a-9607-df406ccd3642",
    "name": "WiFi"
}
```

#### ✅ Test 2.2: Get All Amenities
**Request**: `GET /api/v1/amenities/`

**Response**: `200 OK`
```json
[
    {
        "id": "390f1206-bf37-4b8a-9607-df406ccd3642",
        "name": "WiFi"
    }
]
```

---

### 3. Place Endpoints

#### ✅ Test 3.1: Create Place
**Request**:
```bash
POST /api/v1/places/
Content-Type: application/json

{
    "title": "Cozy Apartment",
    "description": "Nice place",
    "price": 100,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "test-id"
}
```

**Response**: `201 Created`
```json
{
    "id": "93e6d9af-621f-4b2e-ae0a-bad55fc40bb8",
    "title": "Cozy Apartment",
    "description": "Nice place",
    "price": 100,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "test-id"
}
```

#### ✅ Test 3.2: Get All Places
**Request**: `GET /api/v1/places/`

**Response**: `200 OK` - Returns array with all places

---

### 4. Review Endpoints

#### ✅ Test 4.1: Create Review
**Request**:
```bash
POST /api/v1/reviews/
Content-Type: application/json

{
    "text": "Great!",
    "rating": 5,
    "place_id": "test-id",
    "user_id": "test-id"
}
```

**Response**: `201 Created`
```json
{
    "id": "e1bd14b9-fd24-44d3-b8a5-a5da20198099",
    "text": "Great!",
    "rating": 5,
    "place_id": "test-id",
    "user_id": "test-id"
}
```

#### ✅ Test 4.2: Get All Reviews
**Request**: `GET /api/v1/reviews/`

**Response**: `200 OK` - Returns array with all reviews

---

Authors : github.com/h7k2 ; github.com/zoulouhhh
