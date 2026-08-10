# 🛒 E-Commerce Backend

A production-oriented **E-Commerce Backend REST API** built with **FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication**.

The project is being developed using a layered architecture with separation between **API routes, business logic, data access, models, schemas, and security**.

The primary goal of this project is to build a scalable backend while following industry-standard backend development practices.

---

## 🚀 Project Overview

This backend provides the foundation for an e-commerce platform where users will eventually be able to:

- Register and authenticate
- Manage their profiles
- Browse products
- Search and filter products
- Manage shopping carts
- Place orders
- Track order status
- Manage products
- Authenticate using JWT
- Access protected resources
- Handle user roles and permissions
- Interact with a PostgreSQL database

The project is being developed incrementally, with authentication, database architecture, product management, and API design being implemented first.

---

# 🧰 Tech Stack

### Backend

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **JWT Authentication**

### Database

- **PostgreSQL**

### Security

- **JWT**
- **bcrypt**
- Password hashing
- Protected API endpoints

### Development Tools

- **Git**
- **GitHub**
- **Swagger / OpenAPI**
- **Uvicorn**
- **VS Code**

### Planned Infrastructure

- **Docker**
- Docker Compose
- Production environment configuration

---

# 🏗️ Architecture

The project follows a layered backend architecture.

```text
                    Client
                      │
                      ▼
                FastAPI Router
                      │
                      ▼
                  Services
                      │
                      ▼
                Repositories
                      │
                      ▼
                 SQLAlchemy
                      │
                      ▼
                  PostgreSQL

Security-related functionality is separated into dedicated modules.

Authentication Flow

Client
  │
  ▼
/users/login
  │
  ▼
User Service
  │
  ├── Verify Password
  │
  └── Generate JWT
          │
          ▼
        Client
          │
          │ Authorization: Bearer <token>
          ▼
   Protected Endpoint
          │
          ▼
   JWT Verification
          │
          ▼
     Current User

# ⚙️ Application Setup

The FastAPI application is initialized through:

app = FastAPI(...)

The routers are registered in main.py.

Current major routers include:

/users
/products

# 🗄️ Database

The project uses:

PostgreSQL
      │
      ▼
SQLAlchemy
      │
      ▼
FastAPI

SQLAlchemy is used as the ORM to interact with PostgreSQL.

The database layer is responsible for:

Database connection
Session management
ORM models
Database queries
Transactions
Persistent storage

# 🧱 Models

The project currently contains database models for:

Users
Products

More models will be introduced as the e-commerce functionality expands.

Planned models include:

User
Product
Cart
CartItem
Order
OrderItem
Payment
Category

# 📋 Pydantic Schemas

Pydantic is used for request validation and response serialization.

## User Schemas

The project currently contains:

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=100
    )
    full_name: str = Field(
        min_length=2,
        max_length=100
    )

Login schema:

class UserLogin(BaseModel):
    email: EmailStr
    password: str

Response schema:

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }

# 👤 User Management

User functionality is implemented through:

Router
   ↓
User Service
   ↓
User Repository
   ↓
PostgreSQL

# 🔐 Authentication

Authentication is implemented using JWT (JSON Web Tokens).

## Authentication Features

Currently implemented:

User registration
Password hashing
Password verification
JWT generation
JWT expiration
JWT decoding
JWT validation
OAuth2 Bearer token extraction
Current-user dependency
Protected endpoint foundation

# 🔑 Password Security

Passwords are never stored as plain text.

The project uses bcrypt through Passlib.

Password creation:

Plain Password
      │
      ▼
bcrypt hashing
      │
      ▼
Password Hash
      │
      ▼
PostgreSQL

During login:

Password entered by user
          │
          ▼
verify_password()
          │
          ▼
Compare with stored hash

The application only stores the password hash.

# 🔐 JWT Authentication Flow

## The authentication system works as follows:

User
 │
 ▼
POST /users/register
 │
 ▼
Validate UserCreate schema
 │
 ▼
Hash Password
 │
 ▼
User Service
 │
 ▼
User Repository
 │
 ▼
PostgreSQL
 │
 ▼
UserResponse

## Login Flow

User
 │
 ▼
POST /users/login
 │
 ▼
UserLogin Schema
 │
 ▼
User Service
 │
 ▼
Find User by Email
 │
 ▼
Verify Password
 │
 ▼
Create JWT
 │
 ▼
Return Access Token

JWT response:

{
    "access_token": "JWT_TOKEN",
    "token_type": "bearer"
}