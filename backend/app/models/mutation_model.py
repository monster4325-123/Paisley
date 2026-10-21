from pydantic import BaseModel


class MutationRequest(BaseModel):
    accession: str
    mutation: str


class MutationResponse(BaseModel):
    accession: str
    mutation: str
    valid: bool
    message: str

    # Mutation information
    original_amino_acid: str | None = None
    position: int | None = None
    new_amino_acid: str | None = None

    # Structural information
    structure_source: str | None = None
    structure_url: str | None = None
    structure_chain: str | None = None
    structure_residue_number: int | None = None
    structure_residue_name: str | None = None
    structure_coordinates: dict | None = None
    nearby_residues: list[dict] | None = None

    # Amino-acid property comparison
    property_comparison: dict | None = None

    # Explainable interpretation
    interpretation: str | None = None

class MutationPropertyComparison(BaseModel):
    original_name: str
    original_code: str

    mutant_name: str
    mutant_code: str

    original_class: str
    mutant_class: str

    original_charge: str
    mutant_charge: str

    original_polarity: str
    mutant_polarity: str