from fastapi import APIRouter, HTTPException

from app.models.protein_models import (
    ProteinSequenceRequest,
    ProteinSequenceResponse,
)

from app.models.uniprot_model import UniProtResponse
from app.models.alphafold_model import AlphaFoldResponse

from app.services.protein_service import validate_protein_sequence
from app.services.uniprot_service import get_uniprot_protein
from app.services.alphafold_service import get_alphafold_protein

from app.services.rcsb_service import get_rcsb_structure
from app.models.rcsb_model import RCSBResponse

router = APIRouter(
    prefix="/protein",
    tags=["Protein"]
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
def get_protein_from_uniprot(
    accession: str
):
    try:
        return get_uniprot_protein(accession)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get(
    "/alphafold/{accession}",
    response_model=AlphaFoldResponse
)
def get_protein_from_alphafold(
    accession: str
):
    try:
        return get_alphafold_protein(accession)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"AlphaFold service error: {str(error)}"
        )
@router.get(
    "/rcsb/{pdb_id}",
    response_model=RCSBResponse
)
def get_protein_from_rcsb(pdb_id: str):

    result = get_rcsb_structure(pdb_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Structure not found in RCSB PDB."
        )

    return result