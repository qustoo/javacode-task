from uuid import UUID

import pytest
from sqlalchemy import select

from core.models.business_enums import OperationType
from core.models.business_models import WalletHistory


@pytest.mark.asyncio
async def test_wallet_history_deposit_operation(deposit_wallet_for_withdraw, db_session):
    wallet_uuid = UUID(deposit_wallet_for_withdraw["id"])
    stmt = (
        select(WalletHistory.operation_type)
        .where(WalletHistory.wallet_id == wallet_uuid)
        .order_by(WalletHistory.created_at.desc())
        .limit(1)
    )
    wallet_history_operation_type = await db_session.scalar(stmt)
    assert wallet_history_operation_type == OperationType.DEPOSIT


@pytest.mark.asyncio
async def test_wallet_history_withdraw_operation(withdraw_wallet_for_withdraw, db_session):
    wallet_uuid = UUID(withdraw_wallet_for_withdraw["id"])
    stmt = (
        select(WalletHistory.operation_type)
        .where(WalletHistory.wallet_id == wallet_uuid)
        .order_by(WalletHistory.created_at.desc())
        .limit(1)
    )
    wallet_history_operation_type = await db_session.scalar(stmt)
    assert wallet_history_operation_type == OperationType.WITHDRAW
