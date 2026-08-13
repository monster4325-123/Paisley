import requests


def get_rcsb_structure(pdb_id: str):

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id.upper()}"

    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        return None

    response.raise_for_status()

    data = response.json()

    return {
        "pdb_id": pdb_id.upper(),
        "structure_url": f"https://www.rcsb.org/structure/{pdb_id.upper()}",
        "data": data
    }