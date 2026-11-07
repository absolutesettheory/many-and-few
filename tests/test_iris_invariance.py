import math

import pytest

from iris_invariance import (
    create_synthetic_iris,
    dilate_iris,
    extract_iris_dna,
    generate_seal,
)


def test_angular_invariance_T14():
    """
    Theorem T14: the seal is invariant under pupil dilation when the ledger is
    parameterized by normalized angle.
    """
    origin = 0
    partition = ("Interior", "Exterior", "Boundary")

    base_iris = create_synthetic_iris()
    dilated_iris = dilate_iris(base_iris, dilation_factor=1.8)

    dna_base = extract_iris_dna(base_iris)
    dna_dilated = extract_iris_dna(dilated_iris)

    assert dna_base == dna_dilated, "DNA walk failed angular invariance under dilation."

    ledger_base = sum(ord(b) for b in dna_base)
    ledger_dilated = sum(ord(b) for b in dna_dilated)

    seal_base = generate_seal(origin, partition, ledger_base, dna_base)
    seal_dilated = generate_seal(origin, partition, ledger_dilated, dna_dilated)

    assert seal_base == seal_dilated, "Seal failed angular invariance under dilation."


def test_iris_conservation_T13():
    """
    Theorem T13: the accumulated signed valuation remains bounded by the number
    of furrows in the synthetic model.
    """
    base_iris = create_synthetic_iris()
    dna_string = extract_iris_dna(base_iris)

    valuation_map = {"A": 1, "C": 1, "G": -1, "T": -1}
    total_flux = sum(valuation_map[b] for b in dna_string)
    furrow_count = dna_string.count("G")

    assert abs(total_flux) <= furrow_count + 2, "Conservation law violated."


if __name__ == "__main__":
    pytest.main(["-v", __file__])
