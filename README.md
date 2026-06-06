# 🏦 Core Banking System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green.svg)
![SQL%20Server](https://img.shields.io/badge/Database-SQL%20Server-red.svg)
![Architecture](https://img.shields.io/badge/Architecture-Layered%20%7C%20Repository-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)

A multi-layered **Core Banking System** built with Python, SQL Server, and FastAPI that demonstrates enterprise software design principles including the **Repository Pattern**, **Dependency Injection**, **DTO-based communication**, and a **validation pipeline** for enforcing banking rules.

The project supports multiple client applications:

* 🖥️ Desktop Application
* 📱 Mobile Application
* 🌐 REST API

---

# 📖 Overview

This project simulates the core functionality of a banking platform by providing:

* Customer Management
* Employee Management
* Account Management
* Deposits & Withdrawals
* Transaction History
* Authentication & Authorization
* REST API Access
* Desktop User Interface
* Mobile User Interface

The application follows clean architectural principles to ensure maintainability, scalability, and separation of concerns.

---

# 🏗️ Architecture

The system is organized into four primary layers:

```text
┌─────────────────────────────┐
│      Presentation Layer     │
│ Desktop │ Mobile │ API      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Business Logic Layer     │
│ Services │ Validators       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Repository Layer       │
│ Repository Interfaces       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      SQL Server Database    │
└─────────────────────────────┘
```

---

# 🎯 Design Patterns Used

## Repository Pattern

The Repository Pattern abstracts database access from business logic.

Instead of the business layer directly executing SQL queries, it communicates through repository interfaces.

### Benefits

* Loose coupling
* Easier testing
* Cleaner code organization
* Easier database replacement in the future

Example flow:

```text
Controller/UI
      ↓
Business Service
      ↓
Repository Interface
      ↓
SQL Server Repository
      ↓
Database
```

---

## Dependency Injection

Dependencies are injected into services instead of being created internally.

### Benefits

* Better testability
* Reduced coupling
* Improved maintainability

---

## DTO Pattern (Data Transfer Objects)

DTOs are used to transfer data between layers and API endpoints.

### Benefits

* Prevents exposing internal entities
* Improves API consistency
* Simplifies validation

---

## Validation Pipeline / Chain of Responsibility

Transaction validation is performed in a sequential pipeline.

Example:

```text
Validate Amount
        ↓
Validate Account Type
        ↓
Validate Account Status
        ↓
Validate Balance
        ↓
Execute Transaction
```

Each validator is responsible for one rule only, making the system easier to extend and maintain.

---

# 📂 Project Structure

```text
CoreBankingProject
│
├── Presentation
│   ├── Desktop
│   ├── Mobile
│   └── API
│
├── BusinessLogic
│
├── DataAccess
│   └── SQLServerRepositories
│
├── Common
│   ├── DTOs
│   ├── Entities
│   ├── Enums
│   ├── Repositories
│   └── Utilities
│
├── CoreBankingSQLScript.sql
│
├── script
│   └── seed.py
│
├── requirements.txt
│
├── .env
│
├── main.py
├── main_api.py
└── main_mobile.py
```

---

# ⚙️ Prerequisites

Before running the application, ensure you have:

* Python 3.11+
* SQL Server
* SQL Server Management Studio (SSMS)
* Git

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CoreBankingProject.git
cd CoreBankingProject
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

The project dependencies are defined in **requirements.txt**.

```bash
pip install -r requirements.txt
```

---

# 🗄️ Database Setup

## Step 1: Create the Database

Open SQL Server Management Studio and execute:

```text
CoreBankingSQLScript.sql
```

This script creates:

* Tables
* Relationships
* Constraints
* Stored database objects required by the application

---

## Step 2: Configure Environment Variables

Create a `.env` file in the project root directory.

### Example `.env`

```env
# Database Configuration
STORE_MODE=SQLSERVER
SQL_SERVER_DATABASE_SERVER=YOUR_SQL_SERVER_INSTANCE
SQL_SERVER_DATABASE_NAME=CoreBankingDB

# API Security
SECRET_KEY=YOUR_SECRET_KEY

# Email Service (Password Reset)
SENDER_EMAIL=your-email@example.com
SENDER_PASSWORD=your-app-password
```

### Environment Variables Explained

| Variable                     | Description                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `STORE_MODE`                 | Determines which data storage implementation the application uses. The project currently uses `SQLSERVER`. |
| `SQL_SERVER_DATABASE_SERVER` | SQL Server instance name used by the application.                                                          |
| `SQL_SERVER_DATABASE_NAME`   | Name of the Core Banking database.                                                                         |
| `SECRET_KEY`                 | Secret key used by the API for token generation, authentication, and security-related operations.          |
| `SENDER_EMAIL`               | Email address used to send password reset emails.                                                          |
| `SENDER_PASSWORD`            | Email app password used by the password reset service.                                                     |

### Password Reset Email Service

The application includes an email service that sends password reset emails to users.

To use this feature:

1. Enable 2-Factor Authentication on the sender email account.
2. Generate an App Password.
3. Use the generated App Password as the value for `SENDER_PASSWORD`.

---

## Step 3: Seed Initial Data

Once the database schema has been created, run the seed script:

```bash
python script/seed.py
```

The seed script inserts certain initial data required for testing and development.

---

# 🚀 Running the Application

## Desktop Application

```bash
python main.py
```

---

## REST API

```bash
python main_api.py
```

---

## Mobile Application

```bash
python main_mobile.py
```

---

# 🔄 Request Lifecycle

The following diagram shows how data moves through the application:

```text
User
 ↓
Desktop / Mobile / API
 ↓
DTO
 ↓
Business Service
 ↓
Validators
 ↓
Repository Interface
 ↓
SQL Server Repository
 ↓
Database
 ↓
Response
```

---

# 🧪 Suggested Future Enhancements

* Unit Testing Suite
* Integration Testing
* JWT Authentication
* Audit Logging
* Role-Based Access Control (RBAC)
* Docker Support
* CI/CD Pipeline
* Automated Database Migrations
* API Documentation with Swagger Enhancements
* Event-Driven Notifications
* Customer Management
---

# 🔒 Security Notes

* Store secrets in `.env`
* Never commit credentials
* Hash all passwords before storage
* Validate all user input
* Use database transactions for financial operations
* Implement proper authorization checks

---

# 📚 Technologies Used

| Technology                | Purpose                   |
| ------------------------- | ------------------------- |
| Python                    | Backend Development       |
| FastAPI                   | REST API                  |
| SQL Server                | Database                  |
| PyODBC / SQL Connectivity | Database Access           |
| dotenv                    | Environment Configuration |
| Desktop UI Framework      | Desktop Application       |
| Mobile Framework          | Mobile Application        |

---

# 🎓 Educational Objectives

This project demonstrates:

* Layered Architecture
* Repository Pattern
* Dependency Injection
* DTO Pattern
* Validation Pipelines
* SQL Server Integration
* Multi-Frontend Architecture
* Enterprise Application Design Principles

---

# 👨‍💻 Author

Developed as a Core Banking System project to demonstrate modern software engineering practices, architectural patterns, and banking domain workflows.

---

## ⭐ If you found this project useful, consider starring the repository.
