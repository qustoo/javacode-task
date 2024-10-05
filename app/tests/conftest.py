import asyncio
import logging
from typing import Generator
from uuid import UUID

import pytest
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from httpx import AsyncClient

from core.config import settings
from core.database.helper import DatabaseHelper
from core.models.base import Base
from core.models.business_models import Wallet

# dissable logging sqlalchemy for tests session
logging.disable(logging.INFO)


@pytest.fixture(scope="session")
def api_prefix():
    yield settings.api.prefix


# Почистить всю базу перед тестами

@pytest.fixture(scope="session")


@pytest.fixture(scope="session")
async def db_helper():

    assert settings.mode == "TEST"

    url = str(settings.test_database_url)

    helper = DatabaseHelper(url=url)
    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield helper

    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await helper.dispose()


@pytest.fixture(scope="session")
async def db_session(db_helper):
    async with db_helper.session_factory() as session:
        yield session


@pytest.fixture(scope="session")
async def async_client(db_session):
    from main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def redis_connection():
    redis_connection = redis.from_url(f"redis://{settings.redis.host}:{settings.redis.port}", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


@pytest.fixture(scope="session")  # autouse=True)
async def wallet_for_tests(api_prefix, async_client, db_session):
    response = await async_client.post(f"{api_prefix}/wallets/new")
    wallet_uuid = UUID(response.json()["id"])
    yield wallet_uuid
    global_wallet = await db_session.get(Wallet, wallet_uuid)
    await db_session.delete(global_wallet)
    await db_session.commit()


@pytest.fixture(scope="session")
def constant_value():
    return "1000"


@pytest.fixture(scope="session")
async def deposit_wallet_for_withdraw(wallet_for_tests, api_prefix, async_client, db_session, constant_value):
    response = await async_client.post(
        f"{api_prefix}/wallets/{wallet_for_tests}/deposit", json={"amount": constant_value}
    )
    return response.json()


@pytest.fixture(scope="session")
async def withdraw_wallet_for_withdraw(
    wallet_for_tests, deposit_wallet_for_withdraw, api_prefix, async_client, db_session, constant_value
):
    response = await async_client.post(
        f"{api_prefix}/wallets/{wallet_for_tests}/withdraw", json={"amount": constant_value}
    )
    return response.json()
