# Employee Details Backend (Django + Django REST Framework + PostgreSQL)

Welcome! This is the backend API for the **Employee Details System**. It allows the frontend to **store employee details** and **retrieve any employee using their `emp_id` (Primary Key)**.

---

## 🛠️ Tech Stack
- **Python**: 3.14+
- **Django**: 6.1+
- **Django REST Framework (DRF)**: 3.18+
- **Database**: PostgreSQL 18 (with `psycopg` 3)
- **CORS Handling**: `django-cors-headers`

---

## 📂 Project Structure

```
backend/
├── manage.py              # Django command-line management tool
├── setup_db.py            # Helper script to automatically create PostgreSQL database
├── requirements.txt       # Project dependencies
├── .env                   # Configuration & database credentials (password)
├── .env.example           # Template for .env
├── core/                  # Django project configuration
│   ├── settings.py        # Settings (PostgreSQL DB, CORS, DRF, apps)
│   ├── urls.py            # Root URL routing
│   ├── wsgi.py            # WSGI application entry
│   └── asgi.py            # ASGI application entry
└── employees/             # Employees application
    ├── models.py          # Employee database model (emp_id as primary key)
    ├── serializers.py     # DRF Serializer (validates data & JSON conversion)
    ├── views.py           # EmployeeViewSet (Store, Retrieve by emp_id, List)
    ├── urls.py            # Endpoint routing (/api/employees/)
    ├── admin.py           # Django Admin panel configuration
    ├── tests.py           # Automated unit tests
    └── migrations/        # Database migration files
```

---

## 🚀 How to Run the Backend (Step-by-Step for Beginners)

### Step 1: Configure Your PostgreSQL Password
Open the `.env` file in the `backend/` folder:
```env
DB_NAME=employee_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRESQL_PASSWORD_HERE
DB_HOST=127.0.0.1
DB_PORT=5432
```
> Replace `YOUR_POSTGRESQL_PASSWORD_HERE` with the password you set when installing PostgreSQL.

---

### Step 2: Automatically Create the Database
In PowerShell or your terminal, navigate to the `backend` folder and run:
```powershell
python setup_db.py
```
This script will:
1. Connect to your PostgreSQL server.
2. Automatically create the `employee_db` database if it doesn't already exist.
3. Test the connection and confirm everything is ready.

---

### Step 3: Run Database Migrations
Migrations translate the Python model into a real table inside PostgreSQL:
```powershell
python manage.py migrate
```
You will see:
```
Applying employees.0001_initial... OK
```

---

### Step 4: Run the Django Development Server
Start the backend server:
```powershell
python manage.py runserver
```
The server will start at:
👉 **`http://127.0.0.1:8000/`**

---

### Step 5: (Optional) Run Automated Tests
You can verify all endpoints and logic anytime by running:
```powershell
python manage.py test
```

---

### Step 6: (Optional) Create an Admin User
If you want to view records using the Django Admin dashboard:
```powershell
python manage.py createsuperuser
```
Follow the prompts, then visit **`http://127.0.0.1:8000/admin/`** in your browser.

---

## 📡 API Endpoints Reference

| HTTP Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/employees/` | **Store/Create** employee details (also updates if `emp_id` already exists) |
| `GET` | `/api/employees/<emp_id>/` | **Retrieve** employee details by primary key (`emp_id`) |
| `GET` | `/api/employees/` | **List** all registered employees |
| `PUT` | `/api/employees/<emp_id>/` | **Update** all fields of an employee |
| `PATCH` | `/api/employees/<emp_id>/` | **Partial update** of an employee |
| `DELETE` | `/api/employees/<emp_id>/` | **Delete** an employee record |

---

## 📝 Example JSON Payloads

### 1. Store Employee (`POST /api/employees/`)
**Request Body:**
```json
{
  "emp_id": "EMP001",
  "name": "Jane Smith",
  "department": "Engineering",
  "designation": "Software Engineer",
  "email": "jane.smith@example.com",
  "phone": "9876543210"
}
```
*(Note: The API also accepts `"employeeId"` for direct compatibility with the frontend)*

**Success Response (`201 Created` or `200 OK`):**
```json
{
  "message": "Employee 'EMP001' stored successfully.",
  "data": {
    "emp_id": "EMP001",
    "name": "Jane Smith",
    "department": "Engineering",
    "designation": "Software Engineer",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "created_at": "2026-10-12T14:30:00Z",
    "updated_at": "2026-10-12T14:30:00Z"
  }
}
```

### 2. Retrieve Employee by `emp_id` (`GET /api/employees/EMP001/`)
**Success Response (`200 OK`):**
```json
{
  "message": "Employee 'EMP001' retrieved successfully.",
  "data": {
    "emp_id": "EMP001",
    "name": "Jane Smith",
    "department": "Engineering",
    "designation": "Software Engineer",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "created_at": "2026-10-12T14:30:00Z",
    "updated_at": "2026-10-12T14:30:00Z"
  }
}
```

**If Not Found (`404 Not Found`):**
```json
{
  "error": "No employee record found for Employee ID: 'EMP999'"
}
```

---

## 💡 How Everything Works Behind the Scenes

1. **Frontend Request**: When you click *Store Employee* in the Flutter app, Flutter sends an HTTP `POST` request with your employee data encoded as JSON to `http://127.0.0.1:8000/api/employees/`.
2. **URL Router (`urls.py`)**: Django receives the request and routes it to `EmployeeViewSet`.
3. **Serializer (`serializers.py`)**: Checks that all required fields are present, validates email/phone format, and converts the JSON payload into clean Python dictionary data.
4. **Model & PostgreSQL (`models.py`)**: Django ORM executes an SQL `INSERT` or `UPDATE` query into the `employees_employee` table in PostgreSQL, using `emp_id` as the primary key.
5. **Response**: Django sends back a JSON response with status `200` or `201`, which the Flutter app receives and displays in a green success banner!
6. **Retrieval**: When you click *Retrieve by Employee ID*, Flutter sends a `GET` request to `http://127.0.0.1:8000/api/employees/<emp_id>/`. Django runs `SELECT * FROM employees_employee WHERE emp_id = '...'` in PostgreSQL, serializes the result to JSON, and Flutter automatically populates the text fields!
