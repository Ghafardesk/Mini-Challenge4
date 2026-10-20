from typing import Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    url: Optional[str] = None
    output: Optional[str] = None


class ExtractionResult(BaseModel):
    answer: str = ""
    confidence: float = 0.0


class AnswerResponse(BaseModel):
    answer: str = ""
    source_url: str = ""
    confidence: float = 0.0
