# 🏥 Medical Appointment System

## 📌 Project Overview

The **Medical Appointment System** is a backend application built using FastAPI that allows users to manage doctors and appointments efficiently. It supports creating, updating, filtering, and managing appointments along with advanced features like search, sorting, and pagination.

This project demonstrates real-world backend development concepts including API design, validation, business logic handling, and data processing.

---

## 🚀 Features Implemented

### 👨‍⚕️ Doctor Management

* Add new doctors
* Get all doctors
* Get doctor by ID
* Update doctor details (fee, availability)
* Delete doctor (with validation for active appointments)

### 📅 Appointment Management

* Create appointment
* Confirm appointment
* Cancel appointment
* Complete appointment
* View all appointments
* View active appointments (scheduled & confirmed)
* View appointments by doctor

### 🔍 Advanced Features

* Filter doctors (specialization, fee, experience, availability)
* Search doctors (by name or specialization)
* Sort doctors (fee, name, experience)
* Pagination for doctors
* Search appointments (by patient name)
* Sort appointments (by fee/date)
* Pagination for appointments
* Combined browsing (search + sort + pagination)

### 💰 Business Logic

* Fee calculation based on appointment type:

  * Video → 80% of base fee
  * Emergency → 150% of base fee
* Senior citizen discount → 15% extra discount
* Doctor availability automatically updated

---

## 🧠 Backend Concepts Covered

* REST API development with FastAPI
* Request validation using Pydantic
* Path & Query parameters
* Exception handling (HTTPException)
* Business logic implementation
* Data filtering and transformation
* Sorting & pagination
* Route structuring and debugging
* State management using in-memory storage

---

## 🛠 Tech Stack

* **Backend Framework:** FastAPI
* **Language:** Python
* **Validation:** Pydantic
* **Server:** Uvicorn
* **API Testing:** Swagger UI

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sruthilakhotia000/fastapi-medical-appointment-system.git
cd fastapi-medical-appointment-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

```bash
venv\Scripts\activate   # Windows
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

## 📄 API Documentation

Swagger UI available at:
👉 http://127.0.0.1:8000/docs

* Interactive API testing
* Request/Response formats
* All endpoints documented

---

## 📸 Screenshots

All tested API screenshots are available in the **`screenshots/`** folder.

Includes:

* Doctor APIs
* Appointment APIs
* Filter/Search/Sort APIs
* Pagination & Browse APIs

---

## 🎯 Learning Outcomes

Through this project, I learned:

* How to design and build RESTful APIs using FastAPI
* Implementing real-world business logic (fees, discounts, availability)
* Handling errors and debugging API issues
* Working with query parameters for filtering, sorting, and pagination
* Structuring backend projects efficiently
* Understanding API workflows and lifecycle management

---

## 🙌 Acknowledgement

This project was developed as part of the **Agent AI Internship Training at Innomatics Research Labs**.

---

## 📬 Contact

If you have any suggestions or feedback, feel free to connect!
