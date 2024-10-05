from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.helper import database_helper
from core.models.business_models import Wallet


async def get_wallet_object(
    session: Annotated[AsyncSession, Depends(database_helper.session_getter)], wallet_id: UUID = Path(...)
):
    wallet = await session.get(Wallet, wallet_id)
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return wallet
