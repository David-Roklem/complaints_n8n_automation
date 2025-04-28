import enum
from pydantic import BaseModel


class StatusEnum(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class SentimentEnum(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class CategoryEnum(enum.Enum):
    TECHNICAL = "техническая"
    PAYMENT = "оплата"
    OTHER = "другое"


class ComplaintCreate(BaseModel):
    text: str


class ComplaintUpdate(BaseModel):
    id: int
    status: StatusEnum


class ComplaintResponse(ComplaintUpdate):
    sentiment: SentimentEnum
    category: CategoryEnum
