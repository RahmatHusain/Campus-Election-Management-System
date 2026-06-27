# 🗳️ University Election Voting System

> A Python-based command-line application for managing university elections with secure administration, candidate management, and scalable architecture.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/Version-v0.2-blue)
![Status](https://img.shields.io/badge/Status-Day%202%20Completed-success)


---

# 📖 Overview

The **University Election Voting System** is a real-world Python project that simulates the election process in a university. It is designed to evolve into a complete voting platform with authentication, secure voting, reporting, analytics, a GUI, and a web application.

**Day 1** focuses on building the foundation of the project by implementing secure admin authentication, candidate management, and JSON-based data storage.

---

# ✨ Day 1 Features

- 🔐 Secure Admin Login
- 👨‍💼 Role-Based Admin Access
- ➕ Register New Candidates
- 📋 View Registered Candidates
- 💾 Store Candidate Data in JSON
- ⚠️ Basic Error Handling
- 🧩 Modular Python Functions
- 📂 Clean Project Structure

---

# 📂 Project Structure

```text
university-election-voting-system/
│
├── main.py                 # Application entry point
├── config.py               # Constants and configuration
├── database.py             # JSON database operations
├── auth.py                 # Admin & student authentication
├── admin.py                # Admin features
├── student.py              # Student features
├── utils.py                # Helper functions
│
├── data/
│   ├── candidates.json
│   └── students.json
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/RahmatHusain/university-election-voting-system.git
```

## 2️⃣ Navigate to the Project

```bash
cd university-election-voting-system
```

## 3️⃣ Run the Application

```bash
python main.py
```

---

# 🔑 Default Admin Credentials

| Username | Password |
|----------|----------|
| admin | admin123 |

> ⚠️ These credentials are for development purposes only. Secure authentication will be added in future updates.

---
# 📸 Project Preview

## 🏠 Main Menu

```text
==================================================
      UNIVERSITY ELECTION VOTING SYSTEM
==================================================

1. Admin Login
2. Student Registration
3. Student Login
4. Exit

Choose an option:
```

---

## 🔐 Admin Login

```text
Username: admin
Password: ********

✅ Login Successful
```

---

## 👨‍💼 Admin Dashboard

```text
=============== ADMIN MENU ===============

1. Register Candidate
2. View Candidates
3. Logout

Choose:
```

---

## ➕ Register Candidate

```text
Candidate Name : Rahmat Husain
Department     : Computer Science

✅ Candidate Registered Successfully
```

---

## 📋 View Candidates

```text
=============== REGISTERED CANDIDATES ===============

Name       : Rahmat Husain
Department : Computer Science
Votes      : 0

------------------------------------------

Name       : Sarah Khan
Department : Information Technology
Votes      : 0

------------------------------------------
```

---

## 🎓 Student Registration

```text
Student ID : BIT2025001
Name       : Rahul kumar
Department : BIT
Password   : ********

✅ Student Registered Successfully
```

---

## 🔑 Student Login

```text
Student ID : BIT2025001
Password   : ********

✅ Welcome Rahul Husain
```

---

## 📂 Data Storage

### candidates.json

```json
[
    {
        "name": "Rahmat Husain",
        "department": "Computer Science",
        "votes": 0
    },
    {
        "name": "Sarah Khan",
        "department": "Information Technology",
        "votes": 0
    }
]
```

### students.json

```json
[
    {
        "student_id": "BIT2026001",
        "name": "Rahul kumar",
        "department": "BIT",
        "password": "e3b0c44298fc1c149afbf4c8996fb924...",
        "has_voted": false
    }
]
```

---

## ✅ Current Features

- 🔐 Admin Login
- 👨‍💼 Candidate Registration
- 📋 View Candidates
- 🎓 Student Registration
- 🔑 Student Authentication
- 🔒 SHA-256 Password Hashing
- 💾 JSON Data Storage
- ⚠️ Input Validation
- 📂 Modular Project Structure

> 
---

# 🛠️ Technologies Used

- 🐍 Python
- 📄 JSON
- 📂 File Handling
- ⚙️ Functions
- 🔒 getpass Module

---

# 📚 Skills Demonstrated

- Python Programming
- Modular Code Design
- Authentication Logic
- File Handling
- JSON Data Storage
- Error Handling
- Menu-Driven CLI Application

---

# 🗺️ Development Roadmap

- ✅ Day 1 – Admin Login & Candidate Management
- ⏳ Day 2 – Student Registration & Authentication
- ⏳ Day 3 – Voting System & Duplicate Vote Prevention
- ⏳ Day 4 – SQLite Database Integration
- ⏳ Day 5 – Election Results & Winner Declaration
- ⏳ Day 6 – Reports (PDF, CSV & Excel)
- ⏳ Day 7 – Charts, Analytics & Email Notifications
- ⏳ Day 8 – Tkinter GUI & Dark Mode
- ⏳ Day 9 – Flask Web Application & Multi-language Support
- ⏳ Day 10 – Cloud Deployment, Testing & Final Release

---

# 🔮 Upcoming Features

- 🎓 Student Authentication
- 🗳️ Secure Voting System
- 🚫 Duplicate Vote Prevention
- ⏱️ Election Timer
- 🗄️ SQLite Database
- 📊 Live Vote Statistics
- 📈 Graphical Analytics
- 📤 PDF, CSV & Excel Reports
- 📧 Email Notifications
- 📝 Audit Logs
- 🖥️ Modern Tkinter GUI
- 🌐 Flask Web Application
- ☁️ Cloud Deployment
- 🔒 Password Hashing & Data Encryption
- 🌙 Dark Mode
- 🌍 Multi-language Support

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---



# 👨‍💻 Author

## **Rahmat Husain**

🎓 Bachelor of Information Technology (BIT) Student  
💻 Python Developer | Software Development Enthusiast  
🚀 Building **Python Projects** to master Python and create real-world applications.

⭐ **If you like this project, don't forget to star the repository!**
