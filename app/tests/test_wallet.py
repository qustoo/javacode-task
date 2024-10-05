from decimal import Decimal
from uuid import UUID

import pytest

from core.models.business_models import Wallet


@pytest.mark.asyncio
async def test_create_wallet(api_prefix, async_client, db_session):
    response = await async_client.post(f"{api_prefix}/wallets/new")
    created_wallet = response.json()
    database_wallet = await db_session.get(Wallet, created_wallet["id"])

    assert response.status_code == 200
    assert Decimal(created_wallet["balance"]) == 0
    assert database_wallet is not None
    assert database_wallet.id == UUID(created_wallet["id"])
    assert database_wallet.balance == 0

    await db_session.delete(database_wallet)
    await db_session.commit()


@pytest.mark.asyncio
async def test_deposit_wallet(deposit_wallet_for_withdraw, constant_value):
    assert deposit_wallet_for_withdraw["balance"] == constant_value


@pytest.mark.asyncio
async def test_withdraw_wallet(wallet_for_tests, api_prefix, async_client, constant_value):
    response = await async_client.post(
        f"{api_prefix}/wallets/{wallet_for_tests}/withdraw", json={"amount": constant_value}
    )
    wallet = response.json()
    assert wallet["balance"] == "0"


@pytest.mark.asyncio
async def test_withdraw_insufficient_wallet(wallet_for_tests, api_prefix, async_client, constant_value):
    more_then_balance = constant_value * 2
    response = await async_client.post(
        f"{api_prefix}/wallets/{wallet_for_tests}/withdraw", json={"amount": more_then_balance}
    )
    wallet = response.json()
    assert wallet["detail"] == "Insufficient balance"
