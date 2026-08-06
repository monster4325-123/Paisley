from pydantic import BaseModel


class ProteinSequenceRequest(BaseModel):
    sequence: str


class ProteinSequenceResponse(BaseModel):
    valid: bool
    sequence_length: int
    sequence: str
    message: str