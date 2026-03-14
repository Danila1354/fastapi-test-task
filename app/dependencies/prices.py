from datetime import datetime

from fastapi import Query, Depends, HTTPException
from pydantic import ValidationError, AwareDatetime
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.filter import PriceFilterParams
from app.services.ticker import TickerService


def get_price_filters(
    ticker: str = Query(..., description="Currency ticker, e.g. btc_usd"),
    date_from: AwareDatetime | None = Query(None, description="Start of date range"),
    date_to: AwareDatetime | None = Query(None, description="End of date range"),
) -> PriceFilterParams:
    try:
        return PriceFilterParams(ticker=ticker, date_from=date_from, date_to=date_to)
    except ValidationError as e:
        first_error = e.errors()[0]
        raise HTTPException(status_code=422, detail=first_error["msg"])


def get_ticker_service(db: Session = Depends(get_db)) -> TickerService:
    return TickerService(db)
