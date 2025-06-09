
# 💳 NetBank – Full Stack Online Banking System

NetBank is a full-stack online banking system simulation built with Django and MySQL, designed to replicate the core features of a modern banking application. It includes both an **Admin Dashboard** for managing users, cards, and transactions, as well as a **User Dashboard** that offers secure, real-world-like net banking experiences.

---

## 🔧 Features Overview

### 🛡️ Admin Dashboard
A secure panel built for administrative tasks and system oversight.

- **Authentication & Authorization**
  - Role-based access control
  - Secure session management with custom login/logout
- **User Management**
  - Add, view, edit, delete users
  - Clean URL routing using dynamic `user_id`
- **Card Management**
  - Issue new cards (based on card type)
  - Block/Activate/Approve/Replace cards
  - Toggle ATM and Online usage
  - Card detail view with usage/risk insights
- **Transactions**
  - Full transaction history with filtering
  - Drill down using transaction ID
  - Print and PDF download options
- **Utility Functions**
  - Unique Auto Account Number Generator
  - Unique Auto Card Number Generator
  - Unique Auto Transaction ID Generator
- **UI/UX**
  - Responsive design
  - Dark mode support
  - Clean and modern dashboard interface

---

### 👨‍💼 User Dashboard
A dynamic dashboard tailored for end users to perform banking tasks.

- **Authentication**
  - Secure login system
  - Password change functionality
- **Fund Transfers**
  - Transfer money to other users
  - Real-time confirmation with unique transaction ID
- **Transaction Management**
  - Full history view with filters
  - Print/download options for transaction records
- **Card Management**
  - View issued cards
  - Apply for new cards
  - Block, freeze, or activate cards
  - Toggle ATM/Online usage
- **Account & User Info**
  - View personal details, account info, and linked cards
- **UI/UX**
  - Modern, clean interface
  - Fully responsive (mobile + desktop)
  - Dark/light mode toggle

---

## 🛠️ Tech Stack

| Layer        | Technology          |
|--------------|---------------------|
| Backend      | Django (Python)     |
| Frontend     | Django Templates    |
| Database     | MySQL               |
| Auth System  | Django Auth         |
| Planned Next | React Integration (User Dashboard) |

---


## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/omernaseem12/Online-Banking-Application.git
cd mybank
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database Settings

* Open `settings.py`
* Add your MySQL credentials:

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'your_db_name',
          'USER': 'your_mysql_user',
          'PASSWORD': 'your_mysql_password',
          'HOST': 'localhost',
          'PORT': '3306',
      }
  }
  ```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

> Visit `http://127.0.0.1:8000/` to access the site.

---

## 📌 Future Improvements

* React-based frontend for User Dashboard
* Help & Support center with messaging
* Export data to Excel or CSV
* Containerization using Docker
* Live deployment (Render, Railway, etc.)

---

## 🧠 Developer

**Omer Naseem Chaudhry**
🔗 [LinkedIn](www.linkedin.com/in/omer-naseem-chaudhry-909662279)
📫 [your.email@example.com](omernaseem.chaudhry@gmail.com)

---

## ⭐ Show Your Support

If you found this project helpful:

* ⭐ Star this repo
* 🍴 Fork it
* 🧠 Share it with others!

---

## 📜 License

This project is licensed under the **MIT License** – you’re free to use, modify, and build on it.


