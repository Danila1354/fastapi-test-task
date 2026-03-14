from pydantic import BaseModel, model_validator, AwareDatetime
from datetime import datetime


class PriceFilterParams(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    ticker: str
    date_from: AwareDatetime | None = None
    date_to: AwareDatetime | None = None

    @model_validator(mode="after")
    def validate_date_range(self) -> "PriceFilterParams":
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValueError("date_from must be earlier than date_to")
        return self
