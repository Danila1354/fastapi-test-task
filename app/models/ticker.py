from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Ticker(Base):
    __tablename__ = "ticker"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[float] = mapped_column()
