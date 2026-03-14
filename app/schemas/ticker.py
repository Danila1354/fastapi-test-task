from pydantic import BaseModel, ConfigDict, Field


class TickerRead(BaseModel):
    id: int = Field(description="Unique record ID")
    name: str = Field(description="Currency ticker, e.g. btc_usd")
    price: float = Field(description="Index price at the time of recording")
    timestamp: int = Field(description="Unix timestamp of when the price was recorded")
    model_config = ConfigDict(
        from_attributes=True,
    )
