import hashlib
import math


def extract_iris_dna(iris_features, num_angular_steps=64):
    """
    Simulates a DNA walk around the iris by sampling a circular path at a
    normalized radius and mapping observed feature types to nucleotide-like
    symbols.
    """
    dna = []
    for i in range(num_angular_steps):
        theta = (i / num_angular_steps) * 2 * math.pi
        feature = None

        for (r, t), f_type in iris_features.items():
            delta = abs((t - theta + math.pi) % (2 * math.pi) - math.pi)
            if delta < (math.pi / num_angular_steps):
                feature = f_type
                break

        if feature == "crypt":
            dna.append("A")
        elif feature == "collarette":
            dna.append("C")
        elif feature == "furrow":
            dna.append("G")
        elif feature == "pigment":
            dna.append("T")
        else:
            dna.append("A")

    return "".join(dna)


def generate_seal(origin, partition, ledger, dna_string):
    """
    Implements the test's seal construction:
    S(Σ) = H(Ω || repr(π) || repr(Λ)) with the DNA walk folded into the hash.
    """
    state_str = f"{origin}|{partition}|{ledger}|{dna_string}"
    return hashlib.sha256(state_str.encode("utf-8")).hexdigest()


def create_synthetic_iris():
    """Creates a base iris with features at specific angles."""
    return {
        (0.5, 0.0): "collarette",
        (0.5, math.pi / 2): "furrow",
        (0.5, math.pi): "crypt",
        (0.5, 3 * math.pi / 2): "pigment",
    }


def dilate_iris(iris_features, dilation_factor=1.5):
    """
    Simulates pupil dilation while preserving the angular coordinates.
    """
    dilated = {}
    for (r, t), f_type in iris_features.items():
        dilated[(r * dilation_factor, t)] = f_type
    return dilated
