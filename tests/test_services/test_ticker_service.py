import pytest
from unittest.mock import patch
from app.services.ticker import TickerService, TickerNotFoundError


def test_create_ticker(db):
    service = TickerService(db)
    ticker = service.create_ticker("btc_usd", 70000.0)

    assert ticker.id is not None
    assert ticker.name == "btc_usd"
    assert ticker.price == 70000.0
    assert ticker.timestamp is not None


def test_create_ticker_saves_timestamp(db):
    service = TickerService(db)

    with patch("app.services.ticker.time.time") as mock_time:
        mock_time.return_value = 1000
        ticker = service.create_ticker("btc_usd", 70000.0)

    assert ticker.timestamp == 1000


def test_get_latest_price(db):
    service = TickerService(db)

    with patch("app.services.ticker.time.time") as mock_time:
        mock_time.return_value = 1000
        service.create_ticker("btc_usd", 70000.0)
        mock_time.return_value = 2000
        service.create_ticker("btc_usd", 71000.0)

    latest = service.get_latest_price("btc_usd")
    assert latest.price == 71000.0


def test_get_latest_price_not_found(db):
    service = TickerService(db)

    with pytest.raises(TickerNotFoundError):
        service.get_latest_price("btc_usd")


def test_get_all_returns_only_requested_ticker(db):
    service = TickerService(db)
    service.create_ticker("btc_usd", 70000.0)
    service.create_ticker("eth_usd", 3000.0)

    from app.schemas.filter import PriceFilterParams

    results = service.get_all(PriceFilterParams(ticker="btc_usd"))

    assert len(results) == 1
    assert results[0].name == "btc_usd"


def test_get_all_returns_ordered_by_timestamp(db):
    service = TickerService(db)

    with patch("app.services.ticker.time.time") as mock_time:
        mock_time.return_value = 5000
        service.create_ticker("btc_usd", 71000.0)
        mock_time.return_value = 1000
        service.create_ticker("btc_usd", 70000.0)

    from app.schemas.filter import PriceFilterParams

    results = service.get_all(PriceFilterParams(ticker="btc_usd"))

    assert results[0].timestamp == 5000
    assert results[1].timestamp == 1000
