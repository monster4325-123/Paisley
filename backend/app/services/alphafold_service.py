import requests


ALPHAFOLD_API_URL = "https://alphafold.ebi.ac.uk/api/prediction"


def get_alphafold_protein(accession: str):
    """
    Fetch AlphaFold prediction information
    using a UniProt accession.
    """

    url = f"{ALPHAFOLD_API_URL}/{accession}"

    response = requests.get(url, timeout=30)

    if response.status_code == 404:
        raise ValueError(
            f"No AlphaFold structure found for accession {accession}"
        )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(
            f"No AlphaFold prediction available for {accession}"
        )

    prediction = data[0]

    return {
        "accession": accession,
        "entry_id": prediction.get("entryId"),
        "protein_name": prediction.get("uniprotDescription"),
        "gene": prediction.get("gene"),
        "organism": prediction.get("organismScientificName"),
        "confidence": prediction.get("globalMetricValue"),
        "confidence_type": "pLDDT",
        "pdb_url": prediction.get("pdbUrl"),
        "cif_url": prediction.get("cifUrl"),
        "pae_url": prediction.get("paeDocUrl"),
    }