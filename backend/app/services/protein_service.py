from app.models.protein_models import (
    ProteinSequenceRequest,
    ProteinSequenceResponse,
)

# Valid amino acid letters
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def validate_protein_sequence(
    request: ProteinSequenceRequest,
) -> ProteinSequenceResponse:

    # Remove spaces and newlines
    sequence = request.sequence.upper().replace("\n", "").replace(" ", "")

    # Check if empty
    if not sequence:
        return ProteinSequenceResponse(
            valid=False,
            sequence_length=0,
            sequence="",
            message="Protein sequence cannot be empty."
        )

    # Validate amino acids
    if not all(letter in VALID_AMINO_ACIDS for letter in sequence):
        return ProteinSequenceResponse(
            valid=False,
            sequence_length=0,
            sequence=sequence,
            message="Invalid protein sequence. Unknown amino acid detected."
        )

    # Valid sequence
    return ProteinSequenceResponse(
        valid=True,
        sequence_length=len(sequence),
        sequence=sequence,
        message="Valid protein sequence."
    )