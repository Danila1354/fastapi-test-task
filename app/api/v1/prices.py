from typing import List

from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends

from app.dependencies.prices import get_price_filters, get_ticker_service
from app.schemas.filter import PriceFilterParams
from app.schemas.ticker import TickerRead
from app.services.ticker import TickerNotFoundError, TickerService

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get(
    "/",
    response_model=List[TickerRead],
    summary="Get all prices",
    description="Returns all saved prices for the specified ticker, ordered by timestamp descending (newest first). Optionally filter by date range.",
)
async def get_prices(
    filters: PriceFilterParams = Depends(get_price_filters),
    service: TickerService = Depends(get_ticker_service),
):
    return service.get_all(filters)


@router.get(
    "/latest",
    response_model=TickerRead,
    summary="Get latest price",
    description="Returns the most recent price for the specified ticker.",
)
async def get_latest_price(
    service: TickerService = Depends(get_ticker_service),
    ticker: str = Query(..., description="Currency ticker, e.g. btc_usd"),
):
    try:
        return service.get_latest_price(ticker)
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
