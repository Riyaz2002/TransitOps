# TransitOps backend

FastAPI authentication API with PostgreSQL, Alembic, JWT bearer tokens, and role-based access control.

## 1. Create and configure the environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `DATABASE_URL` in `.env`. For AWS RDS, use the RDS endpoint, database user, password, port, and database name, for example:

```env
DATABASE_URL=postgresql+psycopg://transitops_app:URL_ENCODED_PASSWORD@your-db.abc123.ap-south-1.rds.amazonaws.com:5432/transitops
DB_SSL_REQUIRED=true
```

Use a restricted RDS application user, allow inbound port 5432 only from the API's security group, and keep the RDS credentials in your deployment secret manager rather than a committed file.

## 2. Create the schema

```bash
alembic upgrade head
```

For later model changes, create a reviewed migration and apply it:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## 3. Run the API

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. The initial roles are `admin`, `dispatcher`, and `viewer`; new registrations default to `viewer`.

## Auth flow

1. `POST /api/v1/auth/register` creates a viewer account.
2. `POST /api/v1/auth/login` returns an access token.
3. Send `Authorization: Bearer <access_token>` for protected requests.
4. An admin can grant roles using `PATCH /api/v1/users/{user_id}/role`.

Bootstrap the first admin through a controlled database operation after registration, such as `UPDATE users SET role = 'admin' WHERE email = 'you@example.com';`. In production, run this through a one-time operational script or migration, never an open public endpoint.
