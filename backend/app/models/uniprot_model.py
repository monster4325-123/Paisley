from pydantic import BaseModel


class UniProtResponse(BaseModel):
    accession: str
    protein_name: str
    gene: str
    organism: str
    length: int
    sequence: str