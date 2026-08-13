from fastapi import APIRouter
from app.models.uniprot_model import UniProtResponse
from app.services.uniprot_service import get_uniprot_protein

from app.models.protein_models import (
    ProteinSequenceRequest,
    ProteinSequenceResponse,
)

from app.services.protein_service import validate_protein_sequence

router = APIRouter(
    prefix="/protein",
    tags=["Protein"],
)


@router.post(
    "/upload",
    response_model=ProteinSequenceResponse
)
def upload_protein(
    request: ProteinSequenceRequest
):
    return validate_protein_sequence(request)
@router.get(
    "/uniprot/{accession}",
    response_model=UniProtResponse
)
def get_protein_from_uniprot(accession: str):

    return get_uniprot_protein(accession)