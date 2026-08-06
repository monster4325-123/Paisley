from fastapi import APIRouter

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