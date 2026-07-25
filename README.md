# 🏛️ Campus Election Management System (CEMS)

> A secure, transparent, and modern web-based election management system for universities and colleges.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![Status](https://img.shields.io/badge/Status-Day_6-success?style=for-the-badge)

---

# 📌 Project Overview

The **Campus Election Management System (CEMS)** is a secure online voting platform designed for educational institutions. It simplifies election management by providing a transparent, reliable, and user-friendly voting system.

This project is being developed over a **45-Day Professional Development Roadmap**, with new features added daily.

---

# 🚀 Day 1 

## ✅ Completed

- Professional project structure
- Flask project initialization
- SQLite database configuration
- Bootstrap 5 integration
- Base template created
- Landing page created
- Custom CSS added
- Custom 404 & 500 error pages
- Environment configuration
- Project documentation initialized
- GitHub repository setup

🏛️ Campus Election Management System

Day 2/45 Completed ✅

✔ Flask Project Architecture
✔ SQLite Database
✔ User Registration
✔ Password Hashing
✔ WTForms Validation
✔ Bootstrap UI

## ✅ Day 3

- User Login
- Logout
- Flask-Login Authentication
- Protected Dashboard
- Profile Page
- Dynamic Navigation
- Flash Messages
- Session Management
- Responsive UI Improvements


## ✅ Day 4 — Security Enhancement

### Security

- Strong Password Validation
- Confirm Password Validation
- Case-insensitive Login
- Email Normalization
- Failed Login Protection
- Account Lock (5 Attempts)
- Automatic Unlock
- Audit Logging
- Login Activity Tracking
- Environment Variables (.env)
- Session Security
- HTTPOnly Cookies
- SameSite Protection
- Permanent Sessions

### User Features

- Profile Information
- Login Count
- Last Login
- Last Logout

---
## 👥 Role-Based Access Control (RBAC)

## Three different user roles are supported:

- 👑 Super Admin
- 👨‍💼 Election Officer
- 👨‍🎓 Student

- Each role has access only to authorized pages.

## 👑 Super Admin
- Admin Dashboard
- User Management
- Search Users
- Filter Users
- Edit User Role
- Activate / Deactivate Accounts
- Delete Users
- View System Statistics

## 👨‍💼 Election Officer
- Officer Dashboard
- Manage Elections
- Manage Candidates
- Candidate Approvals
- Reports

## 👨‍🎓 Student
- Student Dashboard
- View Election Information
- Profile Management

## 🛡️ Security Features
- Password Hashing
- Login Attempt Limiting
- Account Lock Protection
- Audit Logs
- Role-Based Authorization
- Protected Routes

## 📅 Day 6 – Faculty Management (CRUD)

# Features
✅ Faculty CRUD (Create, Read, Update, Delete)
✅ Activate / Deactivate Faculty
✅ Search Faculty
✅ Filter by Status
✅ Faculty Statistics Dashboard
✅ Responsive Bootstrap UI
✅ Form Validation
✅ Duplicate Name & Code Protection
✅ Role-Based Access Control

# Day 7 


## Completed Module

# Department Management

A complete production-ready Department Management system has been implemented.

---

## Features

✅ Department CRUD

✅ Faculty Relationship

✅ Search

✅ Filter

✅ Statistics Dashboard

✅ Responsive Bootstrap UI

✅ Database Constraints

✅ SQLAlchemy Relationships

✅ Flash Messages

✅ Validation

🎓 Day 8 — Academic Structure Management (Completed)

The Academic Structure module provides a complete university hierarchy and administrative management system.

✅ Implemented Features
✅ Faculty Management
✅ Create Faculty
✅ Edit Faculty
✅ Delete Faculty
✅ Activate/Deactivate Faculty
✅ Search & Filter
✅ Dashboard Statistics
✅ Department Management
✅ Faculty → Department relationship
✅ Department CRUD
✅ Unique department validation
✅ Search & Filter
✅ Responsive dashboard UI
✅ Program Management
✅ Department → Program relationship
✅ Program CRUD
✅ Duration & Semester configuration
✅ Duplicate validation
✅ Active/Inactive status management
✅ Professional admin interface
✅ Academic Year Management
✅ Academic Year CRUD
✅ Current Academic Year management
✅ Date validation rules
✅ Search & Filter
✅ Statistics dashboard
✅ Semester Management
✅ Academic Year → Semester relationship
✅ Semester CRUD
✅ Current Semester management
✅ Active/Inactive toggle
✅ Business validation rules
✅ Search & Filter
✅ Responsive Bootstrap UI
🏗️ Academic Hierarchy

Faculty
└── Department
└── Program
└── Academic Year
└── Semester

Day 9 Progress — Student Management Module
Completed
Academic Hierarchy
Faculty Management
Department Management
Program Management
Academic Year Management
Semester Management
Student System
Student CRUD
Dynamic cascading dropdowns
Student ID & Roll Number generation
Profile dashboard
Verification workflow
Photo upload management
Enterprise Features
Bulk Excel import
Excel export
Duplicate detection
Transaction rollback
Security validation
Permission-based access control
Major Bugs Resolved
Duplicate email validation during edit
Photo upload crash ('str' object has no attribute 'filename')
Jinja template block errors
Missing route endpoint issues
Undefined form field problems
Production Features Achieved
AJAX APIs
ERP-style academic workflow
Verification approval system
Professional Excel reporting
Secure file handling
Database integrity validation

## 🚀 Current Progress

✔ Day 1 Completed

✔ Day 2 Completed

✔ Day 3 Completed

✔ Day 4 Completed

✔ Day 5 Completed

✔ Day 6 Completed

✔ Day 7 Completed

✔ Day 8 Completed

✔ Day 9 Completed

✔ Day 10 Completed

✔ Day 11 Completed


➡️ Next: Day 10 -   Student Management System

# 🛠️ Technology Stack

- 🐍 Python
- 🌐 Flask
- 🗄️ SQLite
- 🎨 HTML5
- 🎨 CSS3
- 🅱️ Bootstrap 5
- 🧩 Jinja2
- 🔒 Flask-WTF (Upcoming)
- 🔐 Flask-Login (Upcoming)
- 📦 SQLAlchemy (Upcoming)

---

# 📂 Project Structure

```text
Campus-Election-Management-System/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── forms/
│   ├── services/
│   ├── utils/
│   ├── static/
│   └── templates/
│
├── database/
├── docs/
├── migrations/
├── tests/
│
├── config.py
├── run.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🎯 Project Goals

- Secure Authentication
- Student Portal
- Admin Dashboard
- Election Management
- Candidate Management
- Online Voting
- Live Results
- Audit Logs
- Reports & Analytics
- Cloud Deployment

---

# 📅 Development Progress

| Day | Status |
|------|--------|
| Day 1 | ✅ Completed |
| Day 2 | ⏳ Authentication System |
| Day 3 | ⏳ User Dashboard |
| Day 4 | ⏳ Election Management |
| Day 5 | ⏳ Candidate Management |

---

# 📸 Current Features

- Responsive Bootstrap UI
- Professional Landing Page
- Flask Application Factory
- SQLite Configuration
- Environment Variables
- Error Handling Pages

---

# 🚧 Upcoming Features

- User Registration
- Secure Login
- Role-Based Access Control
- Student Dashboard
- Admin Dashboard
- Candidate Registration
- Election Scheduling
- Online Voting
- Live Vote Counting
- Charts & Reports

---

# 📖 Documentation

Project documentation is available inside the **docs/** directory.

- PROJECT_ROADMAP.md
- REQUIREMENTS.md
- CHANGELOG.md
- TODO.md

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository and submit a pull request.

--
---

## ⭐ Development Status

**Day 11 Completed Successfully** ✅

**Next Milestone:** Build the complete authentication system with secure login, registration, and role-based access control.
