import math
import requests


def map_residue_to_structure(
    structure_url: str,
    position: int,
    distance_threshold: float = 5.0
):
    """
    Find the target residue and nearby residues
    in an AlphaFold PDB structure.
    """

    response = requests.get(
        structure_url,
        timeout=30
    )

    response.raise_for_status()

    pdb_text = response.text

    # Store atoms grouped by residue
    residues = {}

    for line in pdb_text.splitlines():

        if not line.startswith("ATOM"):
            continue

        try:
            residue_name = line[17:20].strip()
            chain = line[21].strip()
            residue_number = int(line[22:26].strip())

            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())

        except (ValueError, IndexError):
            continue

        residue_key = (
            chain,
            residue_number
        )

        if residue_key not in residues:
            residues[residue_key] = {
                "chain": chain,
                "residue_number": residue_number,
                "residue_name": residue_name,
                "atoms": []
            }

        residues[residue_key]["atoms"].append(
            (x, y, z)
        )

    # Find target residue
    target_key = None

    for key in residues:
        chain, residue_number = key

        if residue_number == position:
            target_key = key
            break

    if target_key is None:
        raise ValueError(
            f"Residue {position} was not found "
            f"in the structure."
        )

    target_residue = residues[target_key]

    # Use the first atom as the representative
    # coordinate returned by the existing API.
    first_atom = target_residue["atoms"][0]

    structure_coordinates = {
        "x": first_atom[0],
        "y": first_atom[1],
        "z": first_atom[2]
    }

    nearby_residues = []

    # Compare target residue against every other residue
    for key, residue in residues.items():

        if key == target_key:
            continue

        minimum_distance = float("inf")

        # Compare every atom of target residue
        # with every atom of the other residue.
        for target_atom in target_residue["atoms"]:

            for other_atom in residue["atoms"]:

                dx = target_atom[0] - other_atom[0]
                dy = target_atom[1] - other_atom[1]
                dz = target_atom[2] - other_atom[2]

                distance = math.sqrt(
                    dx ** 2 +
                    dy ** 2 +
                    dz ** 2
                )

                if distance < minimum_distance:
                    minimum_distance = distance

        if minimum_distance <= distance_threshold:

            nearby_residues.append({
                "chain": residue["chain"],
                "residue_number": residue["residue_number"],
                "residue_name": residue["residue_name"],
                "distance": round(
                    minimum_distance,
                    3
                )
            })

    # Sort closest residues first
    nearby_residues.sort(
        key=lambda residue: residue["distance"]
    )

    return {
        "chain": target_residue["chain"],
        "residue_number": target_residue["residue_number"],
        "residue_name": target_residue["residue_name"],
        "coordinates": structure_coordinates,
        "nearby_residues": nearby_residues
    }