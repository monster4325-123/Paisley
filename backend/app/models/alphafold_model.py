from pydantic import BaseModel
from typing import Optional


class AlphaFoldResponse(BaseModel):
    accession: str
    entry_id: Optional[str] = None
    protein_name: Optional[str] = None
    gene: Optional[str] = None
    organism: Optional[str] = None
    confidence: Optional[float] = None
    confidence_type: str = "pLDDT"
    pdb_url: Optional[str] = None
    cif_url: Optional[str] = None
    pae_url: Optional[str] = None