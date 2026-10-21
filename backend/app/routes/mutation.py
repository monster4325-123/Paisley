from fastapi import APIRouter, HTTPException

from app.models.mutation_model import (
    MutationRequest,
    MutationResponse,
)

from app.services.mutation_service import analyze_mutation


router = APIRouter(
    prefix="/mutation",
    tags=["Mutation"]
)


@router.post(
    "/analyze",
    response_model=MutationResponse
)
def analyze_mutation_route(request: MutationRequest):

    try:
        return analyze_mutation(
            request.accession,
            request.mutation
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Mutation analysis error: {str(error)}"
        )