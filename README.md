# HBnB – Technical Documentation

## Introduction
The **HBnB project** is designed with a **three-layer architecture** that separates responsibilities into distinct layers:  
- **Presentation Layer (API & Services)**: Handles user interaction and exposes endpoints.  
- **Business Logic Layer (Models)**: Encapsulates the domain logic and manages entities like `User`, `Place`, `Review`, and `Amenity`.  
- **Persistence Layer**: Responsible for database operations (storage, retrieval, updates).  

This document compiles the architectural and design diagrams required to guide the implementation of HBnB.  
It includes:  
1. A **High-Level Package Diagram**  
2. A **Detailed Class Diagram** for the Business Logic Layer  
3. **Sequence Diagrams** for core API calls  
4. Explanatory notes  

---

## 1. High-Level Package Diagram

### Diagram
```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +Services
    +API Endpoints
}
class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
}
class PersistenceLayer {
    +Repositories
    +Database Access
}

PresentationLayer --> BusinessLogicLayer : via Facade
BusinessLogicLayer --> PersistenceLayer : Database Operations
Explanation
Presentation Layer: Provides API endpoints and services to external clients. All calls pass through the Facade, which hides the complexity of the underlying system.

Business Logic Layer: Contains the main entities and business rules (validation, relationships, constraints).

Persistence Layer: Provides repositories or DAOs to manage database communication.

The Facade Pattern ensures that the Presentation Layer only interacts with a single entry point into the Business Logic, simplifying communication.

2. Business Logic Layer – Class Diagram
Diagram
mermaid
Copier le code
classDiagram
class User {
    +UUID id
    +String name
    +String email
    +String password
    +Date created_at
    +Date updated_at
    +create()
    +update()
}

class Place {
    +UUID id
    +String name
    +String description
    +String location
    +Float price
    +Date created_at
    +Date updated_at
    +create()
    +update()
}

class Review {
    +UUID id
    +String text
    +Integer rating
    +Date created_at
    +Date updated_at
    +create()
    +update()
}

class Amenity {
    +UUID id
    +String name
    +Date created_at
    +Date updated_at
}

User "1" --> "*" Place : owns >
User "1" --> "*" Review : writes >
Place "1" --> "*" Review : has >
Place "*" --> "*" Amenity : includes >
Explanation
User: Represents the customer, with attributes like email, password, and operations for account management.

Place: Represents listings created by users, with attributes like location and price.

Review: Links users to places with ratings and comments.

Amenity: Represents additional features (e.g., Wi-Fi, pool) associated with places.

Relationships:

A User can own multiple Places.

A User can write multiple Reviews.

A Place can have multiple Reviews.

A Place can have multiple Amenities.

3. Sequence Diagrams – API Calls
3.1 User Registration
mermaid
Copier le code
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Register request (name, email, password)
API->>BusinessLogic: Validate and create User
BusinessLogic->>Database: Insert User record
Database-->>BusinessLogic: Success
BusinessLogic-->>API: User object
API-->>User: Registration success response
3.2 Place Creation
mermaid
Copier le code
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Create Place request
API->>BusinessLogic: Validate request and create Place
BusinessLogic->>Database: Insert Place record
Database-->>BusinessLogic: Success
BusinessLogic-->>API: Place object
API-->>User: Place creation success response
3.3 Review Submission
mermaid
Copier le code
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Submit Review request
API->>BusinessLogic: Validate and create Review
BusinessLogic->>Database: Insert Review record
Database-->>BusinessLogic: Success
BusinessLogic-->>API: Review object
API-->>User: Review submission success response
3.4 Fetching a List of Places
mermaid
Copier le code
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Request list of Places
API->>BusinessLogic: Fetch places by criteria
BusinessLogic->>Database: Query Places
Database-->>BusinessLogic: Place results
BusinessLogic-->>API: Place list
API-->>User: Return Place list (JSON)
4. Conclusion
This document outlines the architecture and design of the HBnB application:

High-Level Package Diagram shows the layered structure and communication via the Facade Pattern.

Business Logic Layer Class Diagram details the entities, their attributes, methods, and relationships.

Sequence Diagrams provide a step-by-step representation of how API calls flow through the system.

This documentation will serve as the blueprint for the project’s implementation and as a reference guide for developers.
