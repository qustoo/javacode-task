from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.helper import database_helper
from core.models.business_models import Wallet


async def get_wallet_object(
        session: Annotated[AsyncSession, Depends(database_helper.session_getter)], wallet_id: UUID = Path(...)
):
    try:
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        scalars_result = await session.scalars(stmt)
        wallet = scalars_result.first()
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
        return wallet
    except OperationalError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Exception: {str(exc)}")
