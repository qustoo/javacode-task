from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.business_enums import OperationType
from core.models.business_models import Wallet, WalletHistory


async def create_wallet(session: AsyncSession):
    new_wallet = Wallet()
    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)
    return new_wallet


async def get_wallet(session: AsyncSession, wallet_id: UUID):
    wallet = await session.get(Wallet, wallet_id)
    return wallet


async def get_wallets(session: AsyncSession):
    stmt = select(Wallet)
    wallets = await session.scalars(stmt)
    return wallets.all()


async def deposit_wallet(session: AsyncSession, wallet: Wallet, transaction_amount: Decimal):
    wallet.balance += transaction_amount
    wallet_history = WalletHistory(wallet_id=wallet.id, operation_type=OperationType.DEPOSIT)
    session.add(wallet_history)
    await session.commit()
    await session.refresh(wallet)
    return wallet


async def withdraw_wallet(session: AsyncSession, wallet: Wallet, transaction_amount: Decimal):
    if wallet.balance < transaction_amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
    wallet.balance -= transaction_amount
    wallet_history = WalletHistory(wallet_id=wallet.id, operation_type=OperationType.WITHDRAW)
    session.add(wallet_history)
    await session.commit()
    await session.refresh(wallet)
    return wallet


async def delete_wallet(session: AsyncSession, wallet: Wallet):
    await session.delete(wallet)
    await session.commit()
