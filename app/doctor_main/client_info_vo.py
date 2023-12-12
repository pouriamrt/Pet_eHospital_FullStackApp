from dataclasses import dataclass
from datetime import datetime


@dataclass
class ClientInfoVo:
    timestamp: datetime
    name: str
    pet_name: str
    pet_type: str
    age : int
    breed: str
    weight: float
    status: str
    client_email: str