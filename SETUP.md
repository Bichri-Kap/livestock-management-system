# Livestock Management System — Development Setup

This guide explains how to set up the Livestock Management System for local development.

The project currently uses:

* **Python 3.12**
* **Django**
* **Django REST Framework**
* **PostgreSQL 16**
* **Docker**
* **Docker Compose**

The application and database run as separate Docker containers.

---

## 1. Prerequisites

Before starting, make sure you have the following installed:

* Git
* Docker Desktop
* Docker Compose

### Windows

If you are developing on Windows, Docker Desktop should have **WSL 2 integration** enabled.

You can verify Docker is working with:

```bash
docker --version
docker compose version
```

Both commands should return version information.

You can also test Docker with:

```bash
docker ps
```

---

## 2. Clone the Repository

Clone the repository:

```bash
git clone <https://github.com/Bichri-Kap/livestock-management-system.git>
```

Then enter the project directory:

```bash
cd livestock-management-system
```

> Replace `<https://github.com/Bichri-Kap/livestock-management-system.git>` with the repository URL provided by the project owner.

---

## 3. Create the Environment File

The project uses environment variables for database configuration.

Create your local `.env` file from the example:

```bash
cp .env.example .env
```

The resulting `.env` should contain:

```env
POSTGRES_DB=livestock
POSTGRES_USER=livestock
POSTGRES_PASSWORD=livestock
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Important

Do **not** commit `.env` to Git.

The `.env` file contains local configuration and is intentionally ignored by Git.

The `.env.example` file is safe to commit and should be kept up to date when new environment variables are introduced.

---

## 4. Start the Application

From the project root, run:

```bash
docker compose up -d
```

This starts the project's Docker services.

Check their status:

```bash
docker compose ps
```

You should see the backend and database services running.

You can also use:

```bash
docker ps
```

---

## 5. Run Database Migrations

After starting the containers, apply the Django database migrations:

```bash
docker compose exec backend python manage.py migrate
```

This creates the required database tables in PostgreSQL.

Whenever new migrations are created during development, apply them using the same command.

---

## 6. Create an Admin User

To access the Django administration interface, create a superuser:

```bash
docker compose exec backend python manage.py createsuperuser
```

Follow the prompts to create the account.

The Django admin interface will be available at:

```text
http://localhost:8000/admin/
```

---

## 7. Access the Application

The Django development server runs on port `8000`.

Open:

```text
http://localhost:8000
```

The Django administration interface is available at:

```text
http://localhost:8000/admin/
```

---

# Development Workflow

## 8. Activate a Python Virtual Environment (Optional)

The application runs inside Docker, so a local Python virtual environment is **not required to run the application**.

However, having a virtual environment can be useful for local development tools, code completion, linting, testing, and IDE support.

From the project root:

```bash
python3 -m venv .venv
```

Activate it on Linux/WSL:

```bash
source .venv/bin/activate
```

The virtual environment is ignored by Git and should not be committed.

---

## 9. Installing Python Dependencies

Python dependencies are defined in:

```text
backend/requirements.txt
```

When dependencies change:

1. Update `requirements.txt`.
2. Rebuild the backend Docker image.

```bash
docker compose build backend
```

Then restart the services:

```bash
docker compose up -d
```

---

## 10. Creating Django Migrations

When Django models are changed, create migrations with:

```bash
docker compose exec backend python manage.py makemigrations
```

Then apply them:

```bash
docker compose exec backend python manage.py migrate
```

Migration files should be committed to Git.

---

## 11. Running Tests

Tests can be run inside the backend container:

```bash
docker compose exec backend python manage.py test
```

As the project grows, automated tests will be added alongside application features.

---

# Useful Docker Commands

### View running services

```bash
docker compose ps
```

### View backend logs

```bash
docker compose logs backend
```

### Follow backend logs

```bash
docker compose logs -f backend
```

### View database logs

```bash
docker compose logs db
```

### Open a shell inside the backend container

```bash
docker compose exec backend bash
```

### Stop the services

```bash
docker compose down
```

### Start the services again

```bash
docker compose up -d
```

### Rebuild the backend

Use this after changing dependencies or the Docker configuration:

```bash
docker compose build backend
```

Then:

```bash
docker compose up -d
```

---

# Git Workflow

## 12. Branches

Do not normally develop directly on `main`.

Create a feature or task branch before making changes:

```bash
git checkout -b feature/<feature-name>
```

For example:

```bash
git checkout -b feature/livestock-registration
```

---

## 13. Before Starting Work

Pull the latest changes:

```bash
git checkout main
git pull origin main
```

Then create your feature branch:

```bash
git checkout -b feature/<feature-name>
```

---

## 14. Commit Changes

Check what has changed:

```bash
git status
```

Stage your changes:

```bash
git add .
```

Commit with a clear message:

```bash
git commit -m "feat: add livestock registration"
```

---

## 15. Push Your Branch

Push your branch to GitHub:

```bash
git push -u origin feature/<feature-name>
```

Open a Pull Request on GitHub when the work is ready for review.

---

# Important Project Rules

* Do not commit `.env`.
* Do not commit `.venv/`.
* Do not commit Python cache files such as `__pycache__/`.
* Do not develop directly on `main` unless explicitly agreed.
* Commit migration files when models change.
* Keep commits focused on a single logical change.
* Pull the latest changes before beginning new work.
* Test changes before opening a Pull Request.

---

# Troubleshooting

## Docker permission denied

If Docker reports a permission error when accessing the Docker socket on Linux/WSL, check whether your user belongs to the `docker` group:

```bash
groups
```

If `docker` is not listed:

```bash
sudo usermod -aG docker $USER
```

Then start a new terminal session.

You can also temporarily refresh the group in the current session with:

```bash
newgrp docker
```

Test with:

```bash
docker ps
```

---

## Backend container is not running

Check the service status:

```bash
docker compose ps
```

Then inspect the backend logs:

```bash
docker compose logs backend
```

---

## Database connection errors

Make sure both services are running:

```bash
docker compose ps
```

The database hostname inside Docker is:

```text
db
```

Do not change `POSTGRES_HOST=db` to `localhost` when Django is running inside Docker.

---

## Changes are not appearing

The backend directory is mounted into the container during development, so most Python code changes should be reflected automatically by Django's development server.

If necessary, restart the backend:

```bash
docker compose restart backend
```

If dependencies or the Docker configuration changed, rebuild:

```bash
docker compose build backend
docker compose up -d
```

---

## Fresh Database

If the local PostgreSQL database needs to be completely reset:

```bash
docker compose down -v
```

Then:

```bash
docker compose up -d
```

**Warning:** `docker compose down -v` deletes the PostgreSQL Docker volume and therefore destroys the local database data.

Only do this when you intentionally want a fresh database.

---

# Current Project Structure

The project currently has the following structure:

```text
livestock-management-system/
├── backend/
│   ├── accounts/
│   ├── config/
│   ├── manage.py
│   ├── Dockerfile
│   └── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── SETUP.md
```

This structure will evolve as additional applications and functionality are introduced.
