# 🗳️ University Election Voting System

> A Python-based command-line application for managing university elections with secure administration, candidate management, and scalable architecture.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/Version-v0.3-blue)

---

# 📖 Overview

The **University Election Voting System** is a real-world Python project that simulates the election process in a university. It is designed to evolve into a complete voting platform with authentication, secure voting, reporting, analytics, a GUI, and a web application.

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
│   ├── students.json
│   └── audit_log.json
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

## 📋 Registered Candidates

```text
=============== REGISTERED CANDIDATES ===============

1. Rahmat Husain
   Department : Computer Science
   Votes      : 0

--------------------------------------------

2. Sarah Khan
   Department : Information Technology
   Votes      : 0

--------------------------------------------
```

---

## 🎓 Student Registration

```text
Student ID : BIT2025001
Name       : Rahmat Husain
Department : BIT
Password   : ********

✅ Student Registered Successfully
```

---

## 🔑 Student Login

```text
Student ID : BIT2025001
Password   : ********

✅ Welcome, Rahmat Husain!
```

---

## 👨‍🎓 Student Dashboard

```text
=============== STUDENT DASHBOARD ===============

1. Cast Vote
2. Logout

Choose:
```

---

## 🗳️ Cast Vote

```text
=============== CANDIDATES ===============

1. Rahmat Husain (Computer Science)
2. Sarah Khan (Information Technology)

Choose Candidate: 2

✅ Vote Cast Successfully!
```

---

## 🚫 Duplicate Vote Prevention

```text
=============== STUDENT DASHBOARD ===============

1. Cast Vote
2. Logout

Choose: 1

❌ You have already voted.
```

---

## 📊 Vote Count

```text
=============== REGISTERED CANDIDATES ===============

1. Rahmat Husain
   Department : Computer Science
   Votes      : 0

--------------------------------------------

2. Sarah Khan
   Department : Information Technology
   Votes      : 1

--------------------------------------------
```

---

## 📝 Audit Log (audit_log.json)

```json
[
    {
        "student_id": "BIT2025001",
        "candidate": "Sarah Khan"
    }
]
```

---

# ✅ Features Completed

- 🔐 Admin Login
- 👨‍💼 Role-Based Admin Access
- ➕ Candidate Registration
- 📋 Candidate Management
- 🎓 Student Registration
- 🔑 Student Authentication
- 🔒 SHA-256 Password Hashing
- 🗳️ Secure Voting System
- 🚫 One Vote Per Student
- 📊 Vote Counting
- 📝 Audit Log
- 💾 JSON Data Storage
- ⚠️ Input Validation & Error Handling
- 🧩 Modular Python Architecture

---

## 🚀 Next Update 

- 🗄️ SQLite Database Integration
- 🔄 Migrate JSON Data to SQLite
- 📊 Improved Vote Counting
- 🏆 Winner Declaration
- ⚡ Faster Data Access
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
