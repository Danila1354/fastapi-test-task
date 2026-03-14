import time
from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.ticker import Ticker
from app.schemas.filter import PriceFilterParams


class TickerNotFoundError(Exception):
    pass


class TickerService:
    def __init__(self, db: Session):
        self.db = db

    def create_ticker(self, ticker_name: str, price: float) -> Ticker:
        ticker = Ticker(name=ticker_name, price=price, timestamp=int(time.time()))
        self.db.add(ticker)
        self.db.commit()
        self.db.refresh(ticker)
        return ticker

    def get_all(self, filters: PriceFilterParams) -> List[Ticker]:
        query = self.db.query(Ticker).filter(Ticker.name == filters.ticker)
        if filters.date_from:
            query = query.filter(Ticker.timestamp >= int(filters.date_from.timestamp()))
        if filters.date_to:
            query = query.filter(Ticker.timestamp <= int(filters.date_to.timestamp()))
        return query.order_by(Ticker.timestamp).all()

    def get_latest_price(self, ticker_name: str) -> Ticker:
        ticker = (
            self.db.query(Ticker)
            .filter(Ticker.name == ticker_name)
            .order_by(desc(Ticker.timestamp))
            .first()
        )
        if not ticker:
            raise TickerNotFoundError(f"Ticker '{ticker_name}' not found")
        return ticker
