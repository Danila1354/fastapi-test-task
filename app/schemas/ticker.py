from pydantic import BaseModel, ConfigDict


class TickerRead(BaseModel):
    id: int
    name: str
    price: float
    timestamp: int
    model_config = ConfigDict(
        from_attributes=True,
    )
