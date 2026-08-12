# E-Commerce Backend API

A production-oriented REST API for an e-commerce platform built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The project implements secure authentication, role-based authorization, product management, shopping cart functionality, transactional checkout, order management, database migrations, automated testing, logging, and containerized deployment.

## Tech Stack

- **Backend:** FastAPI
- **Language:** Python
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Validation:** Pydantic
- **Database Migrations:** Alembic
- **Testing:** Pytest
- **Server:** Uvicorn
- **Containerization:** Docker & Docker Compose
- **Version Control:** Git & GitHub

---

## Features

### Authentication & Authorization
- User registration and login
- Secure password hashing
- JWT-based authentication
- Protected API endpoints
- Role-based access control
- Admin-only operations
- Authenticated user profile endpoint

### Product Management
- Create, read, update, and delete products
- Product search
- Filtering
- Sorting
- Pagination
- Stock management
- Admin-protected product operations

### Shopping Cart
- User-specific shopping carts
- Add products to cart
- Update quantities
- Remove products
- Cart total calculation
- Automatic cart creation for users

### Orders & Checkout
- Transactional checkout process
- Order and OrderItem management
- Stock availability validation
- Automatic inventory reduction
- Cart clearing after successful checkout
- User-specific order history
- Individual order retrieval
- Admin order-status management

### Database & Architecture
- PostgreSQL relational database
- SQLAlchemy ORM
- Foreign-key relationships
- Alembic migration management
- Layered architecture using:
  - Routers
  - Schemas
  - Services
  - Repositories
  - Models

### Reliability & Testing
- Global exception handling
- Centralized application logging
- Automated API tests with Pytest
- Dedicated PostgreSQL test database
- Migration testing against a fresh database

### Deployment
- Dockerized FastAPI application
- PostgreSQL Docker container
- Docker Compose configuration
- Environment-based configuration
- `.env.example` for required environment variables

---

## Project Architecture

```text
app/
├── core/
│   ├── config.py
│   ├── security.py
│   ├── exceptions.py
│   └── logging.py
│
├── db/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   ├── cart_item.py
│   ├── order.py
│   └── order_item.py
│
├── schemas/
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
│
├── repositories/
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── cart_repository.py
│   └── order_repository.py
│
├── services/
│   ├── user_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   └── order_service.py
│
├── routers/
│   ├── users.py
│   ├── products.py
│   ├── cart.py
│   └── orders.py
│
└── main.py

alembic/
├── versions/
└── env.py

tests/
├── conftest.py
├── test_main.py
└── test_users.py

Dockerfile
docker-compose.yml
requirements.txt
.env.example

```
# API Overview

## Authentication

| Method | Endpoint          | Description                    |
| ------ | ----------------- | ------------------------------ |
| POST   | `/users/register` | Register a new user            |
| POST   | `/users/login`    | Authenticate and receive JWT   |
| GET    | `/users/me`       | Get authenticated user profile |

## Products

| Method | Endpoint         | Description                 |
| ------ | ---------------- | --------------------------- |
| POST   | `/products`      | Create product              |
| GET    | `/products`      | List/search/filter products |
| GET    | `/products/{id}` | Get product                 |
| PUT    | `/products/{id}` | Update product              |
| PATCH  | `/products/{id}` | Partially update product    |
| DELETE | `/products/{id}` | Delete product              |

## Cart

| Method | Endpoint                   | Description             |
| ------ | -------------------------- | ----------------------- |
| GET    | `/cart/`                   | Get current user's cart |
| POST   | `/cart/items`              | Add product to cart     |
| PATCH  | `/cart/items/{product_id}` | Update quantity         |
| DELETE | `/cart/items/{product_id}` | Remove product          |

## Orders

| Method | Endpoint                    | Description                 |
| ------ | --------------------------- | --------------------------- |
| POST   | `/orders/checkout`          | Create order from cart      |
| GET    | `/orders/`                  | Get user's orders           |
| GET    | `/orders/{order_id}`        | Get specific order          |
| PATCH  | `/orders/{order_id}/status` | Update order status (Admin) |

# Database Relationships

User
 │
 ├── Cart
 │    └── CartItem ─── Product
 │
 └── Order
      └── OrderItem ─── Product

The checkout workflow validates stock, calculates the order total, creates the order and order items, decreases inventory, and clears the cart within a database transaction.

# Database Migrations

## Alembic manages the complete database schema:

Initial Schema
      ↓
User Role
      ↓
Cart & Cart Items
      ↓
Orders & Order Items

## A fresh PostgreSQL database can be initialized using:

alembic upgrade head

# Testing

The project uses Pytest with a dedicated PostgreSQL test database.

## Run the test suite:

python -m pytest

Current automated coverage includes:

- Root API endpoint
- User registration
- Duplicate email validation
- User login
- JWT generation

# Environment Configuration

## Create a .env file based on .env.example:

DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Sensitive configuration is excluded from version control.

# Running Locally
## 1. Install dependencies
pip install -r requirements.txt

## 2. Configure environment variables
Create .env using .env.example.

## 3. Run database migrations
alembic upgrade head

## 4. Start the API
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

# Docker

The project includes Docker configuration for running the FastAPI application with PostgreSQL.

- docker compose build
- docker compose up

The application and database run as separate containers connected through Docker Compose networking.

Database migrations can be applied inside the application environment with:

- alembic upgrade head

# Design Principles

The backend follows a layered architecture to separate responsibilities:

Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy / PostgreSQL

- Routers handle HTTP requests and responses.
- Schemas validate API input and output.
- Services contain business logic.
- Repositories handle database operations.
- Models define database entities and relationships.
- Core contains shared configuration, security, logging, and exception handling.

This separation improves maintainability, testability, and scalability.

# Security

- Passwords are stored as secure hashes rather than plaintext.
- JWT tokens are used for authentication.
- Protected routes require valid authentication.
- Administrative operations use role-based authorization.
- Secrets are stored through environment variables.
- Sensitive information such as passwords and JWTs is not written to application logs.

# Author

## Harmandeep Nagpal

Built as a production-oriented backend engineering project using modern Python backend technologies.
---