# PostgreSQL Setup Guide

This guide will help you configure the Nook and Care backend to use PostgreSQL instead of SQLite.

## Option 1: Local PostgreSQL Installation

### Step 1: Install PostgreSQL

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer and remember the password you set for the `postgres` user
3. Default port is `5432`

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

Open PostgreSQL command line or pgAdmin and run:

```sql
CREATE DATABASE nookandcare;
```

Or via command line:
```bash
psql -U postgres
CREATE DATABASE nookandcare;
\q
```

### Step 3: Update .env File

Edit your `.env` file and set:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/nookandcare
```

Replace `YOUR_PASSWORD` with the password you set during PostgreSQL installation.

**Example:**
```env
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/nookandcare
```

### Step 4: Run Migrations

```bash
# Activate venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate     # Linux/Mac

# Generate initial migration
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head
```

### Step 5: Seed Data (Optional)

```bash
python -m src.seed.seed_data
```

---

## Option 2: Docker PostgreSQL (Recommended for Development)

### Step 1: Create docker-compose.yml

Create a file named `docker-compose.yml` in the project root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: nookandcare_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: nookandcare
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Step 2: Start PostgreSQL

```bash
docker-compose up -d
```

### Step 3: Update .env File

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nookandcare
```

### Step 4: Run Migrations

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

---

## Option 3: Cloud PostgreSQL (Production)

### Popular Providers:
- **Supabase** (Free tier available): https://supabase.com
- **Neon** (Serverless PostgreSQL): https://neon.tech
- **Railway**: https://railway.app
- **AWS RDS**: https://aws.amazon.com/rds/postgresql/
- **Google Cloud SQL**: https://cloud.google.com/sql

### Example Connection String Format:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

**Supabase Example:**
```env
DATABASE_URL=postgresql://postgres.xxxxx:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## Verify Connection

Test your PostgreSQL connection:

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Start the server
uvicorn src.main:app --reload
```

If the server starts without errors, your PostgreSQL connection is working!

---

## Troubleshooting

### Connection Refused
- Check if PostgreSQL is running: `pg_isready` or check services
- Verify the port (default is 5432)
- Check firewall settings

### Authentication Failed
- Verify username and password in `.env`
- Check PostgreSQL `pg_hba.conf` settings

### Database Does Not Exist
- Create the database: `CREATE DATABASE nookandcare;`

### psycopg2 Installation Issues
The `psycopg2-binary` package is already in `requirements.txt`. If you have issues:

```bash
pip install psycopg2-binary
```

---

## Switching Back to SQLite

If you want to switch back to SQLite for development:

1. Update `.env`:
   ```env
   DATABASE_URL=sqlite:///./dev.db
   ```

2. Delete the SQLite file if it exists:
   ```bash
   rm dev.db
   ```

3. Restart the server (tables will auto-create in dev mode)


