from pydantic import BaseModel
from datetime import datetime


class APIResponse(BaseModel):
    Columns: list[str]
    Description: str
    RowCount: int
    Rows: list[tuple[int, datetime, str]]
