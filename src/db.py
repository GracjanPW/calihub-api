import os
from psycopg_pool import AsyncConnectionPool
from contextlib import asynccontextmanager
from fastapi import FastAPI


DATABASE_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"), 
    "database": os.getenv("DB_NAME"),
}

print(DATABASE_CONFIG)
# Create a global connection pool (but do not open it yet)
pool = AsyncConnectionPool(
    f"postgres://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}",min_size=1, max_size=10, open=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure the connection pool is opened on startup and closed on shutdown."""
    if pool.closed:
        await pool.open()  # ✅ Open the pool
    yield  # ✅ Run the app
    await pool.close()  # ✅ Close the pool on shutdown

async def get_db():
    """Dependency to get a database connection from the pool."""
    if pool.closed:
        await pool.open()  # ✅ Ensure pool is open before using
    async with pool.connection() as conn:
        yield conn