# 📅 Day 3 — Authentication System

## 🎯 Goal

Develop a secure authentication system allowing students to register, log in, log out, and access protected pages.

---

# ✅ Features Implemented

## User Login

- Login form using Flask-WTF
- Email authentication
- Password verification
- Remember Me functionality
- Login validation
- Flash success/error messages

---

## User Logout

- Secure logout
- Session termination
- Redirect to home page
- Success notification

---

## Protected Dashboard

- Dashboard accessible only after login
- Flask-Login `@login_required`
- Unauthorized users redirected to Login page
- Personalized welcome message

---

## Profile Page

Displays:

- Full Name
- Student ID
- Email Address
- User Role
- Registration Date

---

## Navigation Bar

Navbar updates dynamically.

### Guest Users

- Home
- Login
- Register

### Logged-in Users

- Dashboard
- Profile
- Logout

---

## Flash Messages

Implemented Bootstrap alert notifications for:

- Registration Success
- Login Success
- Login Failure
- Logout Success
- Duplicate Email
- Duplicate Student ID

---

## Security

- Password hashing
- Flask-Login session management
- CSRF protection
- Protected routes

---

## UI Improvements

- Responsive Bootstrap layout
- Modern Login page
- Modern Registration page
- Improved Dashboard
- Improved Navbar
- Better Flash Alerts

---

# Testing Completed

✔ Registration

✔ Login

✔ Logout

✔ Session Persistence

✔ Protected Dashboard

✔ Protected Profile

✔ Flash Messages

✔ Navigation Updates

---

# Files Added / Updated

app/routes.py

app/forms/auth_forms.py

app/templates/auth/login.html

app/templates/auth/register.html

app/templates/dashboard.html

app/templates/profile.html

app/templates/layouts/base.html

app/static/css/style.css

---

# Status

Day 3 Completed Successfully

Authentication Module Ready