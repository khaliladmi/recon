from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScanCreate(BaseModel):
    target: str
    mode: str
    tools: List[str]

class ScanRead(BaseModel):
    id: int
    target: str
    mode: str
    tools: List[str]
    start_time: datetime
    end_time: Optional[datetime]
    status: str

    class Config:
        orm_mode = True

