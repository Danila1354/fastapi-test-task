from datetime import datetime, timezone

import pytest
from unittest.mock import patch
from app.services.ticker import TickerService


def test_get_latest_price(db, client):
    service = TickerService(db)
    # Используем mock, потому что, time.sleep() будет замедлять тест, а без time.sleep() тест работает некорректно
    with patch("app.services.ticker.time.time") as mock_time:
        mock_time.return_value = 1000
        service.create_ticker("btc_usd", 70000.0)

        mock_time.return_value = 2000
        service.create_ticker("btc_usd", 71000.0)

    response = client.get("/prices/latest?ticker=btc_usd")

    assert response.status_code == 200
    assert response.json()["price"] == 71000.0


def test_get_latest_price_not_found(client):
    response = client.get("/prices/latest?ticker=btc_usd")
    assert response.status_code == 404


def test_get_latest_price_missing_ticker(client):
    response = client.get("/prices/latest")
    assert response.status_code == 422


def test_get_all_prices(db, client):
    service = TickerService(db)
    service.create_ticker("btc_usd", 70000.0)
    service.create_ticker("btc_usd", 71000.0)
    service.create_ticker("eth_usd", 3000.0)

    response = client.get("/prices/?ticker=btc_usd")
    assert response.status_code == 200
    assert all(res["name"] in "btc_usd" for res in response.json())


def test_get_all_prices_empty(client):
    response = client.get("/prices/?ticker=btc_usd")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_prices_with_date_filter(db, client):
    service = TickerService(db)
    with patch("app.services.ticker.time.time") as mock_time:
        mock_time.return_value = 1000
        service.create_ticker("btc_usd", 70000.0)
        mock_time.return_value = 5000
        service.create_ticker("btc_usd", 71000.0)

    response = client.get(
        "/prices/?ticker=btc_usd&date_from=1970-01-01T00:16:00Z&date_to=1970-01-01T00:17:00Z"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    assert response.json()[0]["price"] == 70000.0


def test_get_all_prices_invalid_date_range(client):
    response = client.get(
        "/prices/?ticker=btc_usd&date_from=2026-03-14T23:00:00&date_to=2026-03-14T01:00:00"
    )
    assert response.status_code == 422
