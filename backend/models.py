from pydantic import BaseModel
from typing import Optional

class Passenger(BaseModel):
    ticket: str
    first_name: str
    last_name: str

class DownloadResult(BaseModel):
    success: bool
    message: Optional[str] = None
    file_name: Optional[str] = None
