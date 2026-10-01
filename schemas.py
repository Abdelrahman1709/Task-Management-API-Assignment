from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    priority: Literal["low", "medium", "high"]
    description: Optional[str] = "No description"

    @field_validator("title")
    @classmethod
    def validate_title_uppercase(cls, v: str) -> str:
        if not v or not v[0].isupper():
            raise ValueError("Title must start with an uppercase letter")
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    priority: Optional[Literal["low", "medium", "high"]] = None
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title_uppercase_if_provided(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if len(v) == 0 or not v[0].isupper():
                raise ValueError("Title must start with an uppercase letter")
        return v


class TaskResponse(BaseModel):
    task_id: int
    title: str
    priority: str
    description: str
    status: str