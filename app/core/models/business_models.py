from uuid import UUID

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.business_enums import OperationType


class Wallet(Base):
    __tablename__ = "wallet"
    __table_args__ = (CheckConstraint("balance >= 0", name="check_balance_non_negative"),)

    balance: Mapped["Numeric"] = mapped_column(Numeric, nullable=False, default=0)
    wallet_history: Mapped["WalletHistory"] = relationship(
        "WalletHistory", back_populates="wallet", cascade="all, delete-orphan"
    )


class WalletHistory(Base):
    __tablename__ = "wallet_history"

    wallet_id: Mapped[UUID] = mapped_column(ForeignKey("wallet.id", ondelete="CASCADE"), nullable=False)
    operation_type: Mapped["OperationType"] = mapped_column(Enum(OperationType), nullable=False)

    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="wallet_history")
