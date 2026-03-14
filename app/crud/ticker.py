import time

from sqlalchemy.orm import Session
from app.models.ticker import Ticker


def create_ticker(db: Session, index_name: str, price: float):
    ticker = Ticker(name=index_name, price=price, timestamp=time.time())
    db.add(ticker)
    db.commit()
    db.refresh(ticker)
    return ticker
