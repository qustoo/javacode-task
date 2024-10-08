from typing import Annotated, List
from uuid import UUID

from api.wallet import crud
from api.wallet.dependices import get_wallet_object
from core.database.helper import database_helper
from core.schemas.wallet import Transaction, WalletResponse
from fastapi import APIRouter, Depends, Path
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

wallet_router = APIRouter(prefix="/wallets", tags=["wallets"])


@wallet_router.post("/new", response_model=WalletResponse)
async def create_wallet(session: Annotated[AsyncSession, Depends(database_helper.session_getter)]):
    return await crud.create_wallet(session)


@wallet_router.get("/", response_model=List[WalletResponse])
async def get_all_wallets(session: Annotated[AsyncSession, Depends(database_helper.session_getter)]):
    return await crud.get_wallets(session)


@wallet_router.get("/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet_balance(
    session: Annotated[AsyncSession, Depends(database_helper.session_getter)], wallet_uuid: Annotated[UUID, Path(...)]
):
    return await get_wallet_object(session, wallet_uuid)


@wallet_router.post(
    "/{wallet_uuid}/deposit", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=WalletResponse
)
async def deposit_wallet(
    session: Annotated[AsyncSession, Depends(database_helper.session_getter)],
    wallet_uuid: Annotated[UUID, Path(...)],
    transaction: Transaction,
):
    wallet = await get_wallet_object(session, wallet_uuid)
    return await crud.deposit_wallet(session, wallet, transaction.amount)


@wallet_router.post(
    "/{wallet_uuid}/withdraw", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=WalletResponse
)
async def withdraw_wallet(
    session: Annotated[AsyncSession, Depends(database_helper.session_getter)],
    wallet_uuid: Annotated[UUID, Path(...)],
    transaction: Transaction,
):
    wallet = await get_wallet_object(session, wallet_uuid)
    return await crud.withdraw_wallet(session, wallet, transaction.amount)


@wallet_router.delete("/{wallet_uuid}/", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def remove_wallet(
    session: Annotated[AsyncSession, Depends(database_helper.session_getter)],
    wallet_uuid: Annotated[UUID, Path(...)],
):
    wallet = await get_wallet_object(session, wallet_uuid)
    return await crud.delete_wallet(session, wallet)
