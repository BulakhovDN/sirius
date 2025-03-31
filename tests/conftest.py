import asyncio
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from db.database import get_db
from main import app

TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres_test:postgres_test@127.0.0.1:5436/postgres_test"
)


CLEAN_TABLES = [
    "leaves",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    text(
                        f"""TRUNCATE TABLE {table_for_cleaning} RESTART IDENTITY CASCADE;"""
                    )
                )


async def _get_test_db():
    test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

    test_async_session_make = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )

    async with test_async_session_make() as test_async_session:
        yield test_async_session


@pytest.fixture(scope="function")
async def client():
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client
