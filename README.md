# 🏃‍♂️ Athletics Competition Manager

A web application for managing athletics competitions. Built as part of a final thesis project using Django, PostgreSQL, Vue 3, TypeScript, Vite, Bootstrap, and Docker Compose, etc.

---

## 1. Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps to Run

1. **Clone the repository:**

```bash
git clone <repo_url>
cd FinalThesis_AthleticsManager
```

2. **Start containers:**

```bash
docker compose up --build
```

This launches:
- Frontend at: [http://localhost:5173](http://localhost:5173)
- Backend (Django + admin): [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 2. Running Migrations

If you're starting on a new environment (e.g., after `git clone`), the database will be empty.

1. Enter the backend container:

```bash
docker compose exec backend sh
```

2. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 3. Creating a Superuser

To access the admin interface, create a superuser (inside backend container):

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

---

## 4. Application URLs

| Module      | URL                                    |
|-------------|----------------------------------------|
| Frontend    | http://localhost:5173                  |
| Admin panel | http://localhost:8000/admin            |
| Swagger     | http://localhost:8000/api/docs/swagger |
| ReDoc       | http://localhost:8000/api/docs/redoc   |

If hosted on a VPS (e.g. `173.123.123.321`), replace `localhost` with the IP address.

---

## 5. Testing

### Backend: Unit Tests

Run all Django unit tests using:

```bash
docker compose exec backend python manage.py test apps.m403.tests.test_all_tests
```

This includes model, view, and filter tests.

### Few Frontend (Vitest)

To run frontend tests:


```bash
docker compose exec frontend npx vitest run
```

---

