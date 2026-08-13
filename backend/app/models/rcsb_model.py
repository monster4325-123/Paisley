from pydantic import BaseModel
from typing import Optional, Dict, Any


class RCSBResponse(BaseModel):
    pdb_id: str
    structure_url: str
    data: Optional[Dict[str, Any]] = None