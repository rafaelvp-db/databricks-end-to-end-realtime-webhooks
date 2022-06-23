from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    ID: int
    AN3: float
    AN4: float
    AN5: float
    AN6: float
    AN7: float
    AN8: float
    AN9: float
    AN10: float
    SPEED: float
    TORQUE: Optional[int] = None
    TIMESTAMP: str