import re

from app.services.uniprot_service import get_uniprot_protein
from app.services.alphafold_service import get_alphafold_protein
from app.services.structure_mapping_service import (
    map_residue_to_structure
)
from app.services.amino_acid_service import (
    get_amino_acid_properties
)

def build_mutation_interpretation(
    original_properties,
    mutant_properties,
    position,
    nearby_residues
):
    original_name = original_properties["name"]
    mutant_name = mutant_properties["name"]

    original_code = original_properties["code"]
    mutant_code = mutant_properties["code"]

    original_class = original_properties["class"]
    mutant_class = mutant_properties["class"]

    original_charge = original_properties["charge"]
    mutant_charge = mutant_properties["charge"]

    original_polarity = original_properties["polarity"]
    mutant_polarity = mutant_properties["polarity"]

    nearby_count = len(nearby_residues)

    interpretation = (
        f"The mutation {original_code}{position}{mutant_code} "
        f"replaces {original_name} with {mutant_name}. "
        f"Both residues are classified as {original_class.lower()} "
        f"and {mutant_class.lower()}, respectively. "
        f"The charge property changes from "
        f"{original_charge.lower()} to {mutant_charge.lower()}, "
        f"while polarity changes from "
        f"{original_polarity.lower()} to "
        f"{mutant_polarity.lower()}. "
        f"The mutated residue has {nearby_count} "
        f"nearby residues identified within the analyzed "
        f"structural neighborhood."
    )

    return interpretation

def analyze_mutation(accession: str, mutation: str):

    accession = accession.strip().upper()
    mutation = mutation.strip().upper()

    # --------------------------------------------------
    # 1. Check mutation format
    # --------------------------------------------------
    match = re.fullmatch(
        r"([A-Z])(\d+)([A-Z])",
        mutation
    )

    if not match:
        raise ValueError(
            "Invalid mutation format. Use format like R175H."
        )

    original_amino_acid = match.group(1)
    position = int(match.group(2))
    new_amino_acid = match.group(3)

    # --------------------------------------------------
    # 2. Fetch protein from UniProt
    # --------------------------------------------------
    protein = get_uniprot_protein(accession)

    sequence = protein.sequence

    # --------------------------------------------------
    # 3. Check mutation position
    # --------------------------------------------------
    if position < 1 or position > len(sequence):
        raise ValueError(
            f"Mutation position {position} is outside "
            f"the protein sequence length ({len(sequence)})."
        )

    # UniProt sequence positions are 1-based
    actual_amino_acid = sequence[position - 1]

    # --------------------------------------------------
    # 4. Get amino-acid properties
    # --------------------------------------------------
    original_properties = get_amino_acid_properties(
        original_amino_acid
    )

    mutant_properties = get_amino_acid_properties(
        new_amino_acid
    )

    # --------------------------------------------------
    # 5. Check whether mutation matches the real sequence
    # --------------------------------------------------
    if actual_amino_acid != original_amino_acid:

        return {
            "accession": accession,
            "mutation": mutation,
            "valid": False,
            "message": (
                f"Position {position} contains "
                f"{actual_amino_acid}, not "
                f"{original_amino_acid}."
            ),
            "original_amino_acid": actual_amino_acid,
            "position": position,
            "new_amino_acid": new_amino_acid,
        }

    # --------------------------------------------------
    # 6. Fetch AlphaFold structure information
    # --------------------------------------------------
    alphafold = get_alphafold_protein(accession)

    # --------------------------------------------------
    # 7. Map mutation to structure
    # --------------------------------------------------
    structure_mapping = map_residue_to_structure(
        alphafold.get("pdb_url"),
        position
    )
    interpretation = build_mutation_interpretation(
      original_properties,
      mutant_properties,
      position,
      structure_mapping.get("nearby_residues", [])
    )

    # --------------------------------------------------
    # 8. Return complete mutation analysis
    # --------------------------------------------------
    return {

        # Basic mutation information
        "accession": accession,
        "mutation": mutation,
        "valid": True,
        "message": "Mutation validated successfully.",

        "original_amino_acid": original_amino_acid,
        "position": position,
        "new_amino_acid": new_amino_acid,

        # --------------------------------------------------
        # Amino-acid property comparison
        # --------------------------------------------------
        "property_comparison": {

            "original_name":
                original_properties["name"],

            "original_code":
                original_amino_acid,

            "mutant_name":
                mutant_properties["name"],

            "mutant_code":
                new_amino_acid,

            "original_class":
                original_properties["class"],

            "mutant_class":
                mutant_properties["class"],

            "original_charge":
                original_properties["charge"],

            "mutant_charge":
                mutant_properties["charge"],

            "original_polarity":
                original_properties["polarity"],

            "mutant_polarity":
                mutant_properties["polarity"],
        },

        "interpretation": interpretation,

        # --------------------------------------------------
        # Structural information
        # --------------------------------------------------
        "structure_source": "AlphaFold",

        "structure_url":
            alphafold.get("pdb_url"),

        "structure_chain":
            structure_mapping.get("chain"),

        "structure_residue_number":
            structure_mapping.get("residue_number"),

        "structure_residue_name":
            structure_mapping.get("residue_name"),

        "structure_coordinates":
            structure_mapping.get("coordinates"),

        "nearby_residues":
            structure_mapping.get("nearby_residues"),
    }