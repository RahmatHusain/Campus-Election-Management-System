# Day 6 Documentation – Faculty Management (CRUD)

## Project

**Campus Election Management System (CEMS)**

## Phase

Phase 2 – University Management

## Day

Day 6 – Faculty Management (CRUD)

---

# Objective

The goal of Day 6 was to build a complete Faculty Management module that allows the Super Admin to manage university faculties. This module serves as the foundation for Department Management in Day 7.

---

# Features Implemented

## ✅ Faculty Database Model

Created a Faculty model with the following fields:

* id
* name
* code
* description
* is_active
* created_at

Added SQLAlchemy model relationships and a readable `__repr__()` method.

---

## ✅ Database Migration

Successfully created and applied database migration.

Commands used:

```bash
flask db migrate -m "Create faculties table"
flask db upgrade
```

Verified that the database contains the `faculties` table.

---

## ✅ Faculty Form

Implemented Flask-WTF form with:

* Faculty Name
* Faculty Code
* Description
* Active Status

Validation includes:

* Required fields
* Unique faculty name
* Unique faculty code

---

## ✅ Faculty CRUD

Implemented the following routes:

* View Faculties
* Create Faculty
* Edit Faculty
* Delete Faculty
* Activate Faculty
* Deactivate Faculty

Access is restricted to Super Admin users.

---

## ✅ Faculty Interface

Created a responsive Bootstrap interface including:

* Statistics cards
* Faculty listing
* Search bar
* Status filter
* Edit button
* Delete button
* Activate / Deactivate button

---

## ✅ Search & Filter

Implemented search by:

* Faculty Name
* Faculty Code

Status filter:

* All
* Active
* Inactive

---

## ✅ Dashboard Statistics

Statistics cards display:

* Total Faculties
* Active Faculties
* Inactive Faculties

---

## ✅ Validation

Implemented protection against:

* Duplicate faculty names
* Duplicate faculty codes
* Empty form submission

---

## ✅ Navigation

Added Faculty Management to the Admin Sidebar.

Navigation now includes:

* Dashboard
* Users
* Faculties
* Departments (placeholder)
* Reports
* Settings

---

# Technologies Used

* Python
* Flask
* SQLAlchemy
* Flask-WTF
* Flask-Login
* Bootstrap 5
* SQLite
* Jinja2

---

# Challenges Solved

During development the following issues were resolved:

* Duplicate faculty validation
* SQLAlchemy IntegrityError
* Flask migration setup
* Flask-Migrate configuration
* Blueprint registration conflict
* Jinja template errors
* URL BuildError
* Faculty activation logic
* Template rendering issues
* Search and filter improvements

---

# Result

Day 6 has successfully delivered a complete Faculty Management module with secure CRUD operations, validation, statistics, search, filtering, and a responsive administrative interface.

The project is now ready to continue with **Day 7 – Department Management**.
