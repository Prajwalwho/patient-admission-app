# Patient Admission Management App

A web app for hospital staff to manage admitted patients: add, view, filter, search, edit, delete (with confirmation) and discharge. Built for the DScribe Software Engineer Intern Round 1 task.

## Live Links

| | URL |
|---|---|
| Frontend (live app) | https://patient-admission-app-iota.vercel.app |
| Backend API | https://patient-admission-api-poxm.onrender.com |
| API docs (Swagger) | https://patient-admission-api-poxm.onrender.com/docs |
| GitHub repo | https://github.com/Prajwalwho/patient-admission-app |

> **Note:** The backend runs on Render's free tier and sleeps when idle. The first request after a pause can take 30 to 60 seconds. Please wait and refresh once. After that it responds normally.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), Axios, plain CSS (responsive) |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL (Neon, hosted), data persists across server restarts |
| Deployment | Vercel (frontend), Render (backend) |

## Features

- Add, view, edit and delete patients (delete asks for confirmation)
- Mark a patient as Discharged
- Filter by Ward, Department and Doctor (filters can be combined)
- Search patients by name (case-insensitive)
- Responsive design: card layout on mobile, compact table on tablet, full table on desktop
- Validation in **both** frontend and backend, with clear error messages

## Validation Rules

| Field | Rule |
|---|---|
| Name | Required, letters (and spaces) only |
| Age | Required, whole number from 0 to 120 |
| Gender, Ward, Department, Doctor | Required, must be one of the listed options |
| Admission Date | Required, cannot be a future date (checked in IST) |

The backend rejects invalid data with HTTP 422 and a response like:

```json
{
  "message": "Validation failed",
  "errors": { "age": "Age must be a whole number between 0 and 120" }
}
```

## Project Structure

```
patient-admission-app/
├── backend/
│   ├── app/
│   │   ├── main.py          # app, CORS, error handlers
│   │   ├── database.py      # DB engine and session
│   │   ├── models.py        # Patient table
│   │   ├── schemas.py       # Pydantic validation
│   │   ├── constants.py     # dropdown values
│   │   └── routers/patients.py   # API endpoints
│   ├── test_api.py, test_model.py, test_validation.py, test_db.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── api/client.js
│       ├── components/      # PatientTable, PatientForm, Filters, ConfirmDialog
│       ├── utils/validation.js
│       ├── App.jsx
│       └── index.css
└── docs/screenshots/
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/options` | Dropdown values (genders, wards, departments, doctors) |
| POST | `/patients` | Add a patient |
| GET | `/patients?ward=&department=&doctor=&search=` | List with filters and name search |
| GET | `/patients/{id}` | Get one patient |
| PUT | `/patients/{id}` | Edit a patient |
| DELETE | `/patients/{id}` | Delete a patient |
| PATCH | `/patients/{id}/discharge` | Mark as Discharged |

## Run Locally

**Prerequisites:** Python 3.11+, Node.js 18+, and a PostgreSQL database (a free [Neon](https://neon.tech) project works).

### 1. Clone

```bash
git clone https://github.com/Prajwalwho/patient-admission-app.git
cd patient-admission-app
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env` (copy from `.env.example`):

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
FRONTEND_URL=http://localhost:5173
```

Run the server (tables are created automatically on startup):

```bash
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000, docs: http://127.0.0.1:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

```bash
npm run dev
```

App: http://localhost:5173

### 4. Run the tests (backend)

```bash
cd backend
python test_validation.py   # validation rules
python test_api.py          # all endpoints against the configured database
```

## Screenshots

### Desktop
![Desktop patient list](docs/screenshots/desktop-list.png)

### Filters and search
![Filters and search](docs/screenshots/filters-search.png)

### Add patient with validation errors
![Add patient form](docs/screenshots/add-form.png)

### Delete confirmation
![Delete confirmation](docs/screenshots/delete-confirm.png)

### Tablet
![Tablet view](docs/screenshots/tablet.png)

### Mobile
![Mobile view](docs/screenshots/mobile.jpeg)

## Security

No passwords or secret keys are committed. Credentials are read from environment variables; see the `.env.example` files.

## Author

PRAJWAL SINGH