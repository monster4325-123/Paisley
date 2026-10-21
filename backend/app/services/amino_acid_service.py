AMINO_ACID_PROPERTIES = {

    "A": {
        "name": "Alanine",
        "code": "A",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "R": {
        "name": "Arginine",
        "code": "R",
        "class": "Basic",
        "charge": "Positive",
        "polarity": "Polar",
    },

    "N": {
        "name": "Asparagine",
        "code": "N",
        "class": "Polar",
        "charge": "Neutral",
        "polarity": "Polar",
    },

    "D": {
        "name": "Aspartic acid",
        "code": "D",
        "class": "Acidic",
        "charge": "Negative",
        "polarity": "Polar",
    },

    "C": {
        "name": "Cysteine",
        "code": "C",
        "class": "Polar",
        "charge": "Neutral",
        "polarity": "Polar",
    },

    "E": {
        "name": "Glutamic acid",
        "code": "E",
        "class": "Acidic",
        "charge": "Negative",
        "polarity": "Polar",
    },

    "Q": {
        "name": "Glutamine",
        "code": "Q",
        "class": "Polar",
        "charge": "Neutral",
        "polarity": "Polar",
    },

    "G": {
        "name": "Glycine",
        "code": "G",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "H": {
        "name": "Histidine",
        "code": "H",
        "class": "Basic",
        "charge": "Variable",
        "polarity": "Polar",
    },

    "I": {
        "name": "Isoleucine",
        "code": "I",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "L": {
        "name": "Leucine",
        "code": "L",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "K": {
        "name": "Lysine",
        "code": "K",
        "class": "Basic",
        "charge": "Positive",
        "polarity": "Polar",
    },

    "M": {
        "name": "Methionine",
        "code": "M",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "F": {
        "name": "Phenylalanine",
        "code": "F",
        "class": "Aromatic",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "P": {
        "name": "Proline",
        "code": "P",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "S": {
        "name": "Serine",
        "code": "S",
        "class": "Polar",
        "charge": "Neutral",
        "polarity": "Polar",
    },

    "T": {
        "name": "Threonine",
        "code": "T",
        "class": "Polar",
        "charge": "Neutral",
        "polarity": "Polar",
    },

    "W": {
        "name": "Tryptophan",
        "code": "W",
        "class": "Aromatic",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },

    "Y": {
        "name": "Tyrosine",
        "code": "Y",
        "class": "Aromatic",
        "charge": "Neutral",
        "polarity": "Polar",
    },

    "V": {
        "name": "Valine",
        "code": "V",
        "class": "Nonpolar",
        "charge": "Neutral",
        "polarity": "Nonpolar",
    },
}


def get_amino_acid_properties(code: str):

    properties = AMINO_ACID_PROPERTIES.get(
        code.upper()
    )

    if properties is None:
        raise ValueError(
            f"Unknown amino acid code: {code}"
        )

    return properties