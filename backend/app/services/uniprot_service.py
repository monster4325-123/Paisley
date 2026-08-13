import requests

from app.models.uniprot_model import UniProtResponse


def get_uniprot_protein(accession: str) -> UniProtResponse:

    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"

    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError("Protein not found in UniProt.")

    response.raise_for_status()

    data = response.json()

    protein_name = (
        data.get("proteinDescription", {})
        .get("recommendedName", {})
        .get("fullName", {})
        .get("value", "Unknown")
    )

    gene = (
        data.get("genes", [{}])[0]
        .get("geneName", {})
        .get("value", "Unknown")
    )

    organism = data.get("organism", {}).get(
        "scientificName",
        "Unknown"
    )

    sequence_data = data.get("sequence", {})

    sequence = sequence_data.get("value", "")

    length = sequence_data.get(
        "length",
        len(sequence)
    )

    return UniProtResponse(
        accession=data.get(
            "primaryAccession",
            accession
        ),
        protein_name=protein_name,
        gene=gene,
        organism=organism,
        length=length,
        sequence=sequence,
    )