from utils.sequence_utils import pad_sequence, get_all_taxa, ensure_consistent_length

def test_pad_sequence():
    assert pad_sequence("ACT", 5) == "ACT??"
    assert pad_sequence("ACTG", 4) == "ACTG"
    assert pad_sequence("A", 3, "-") == "A--"

def test_get_all_taxa():
    seq_dicts = [
        {"Taxon1": "AAA", "Taxon2": "CCC"},
        {"Taxon2": "GGG", "Taxon3": "TTT"}
    ]
    taxa = get_all_taxa(seq_dicts)
    assert taxa == {"Taxon1", "Taxon2", "Taxon3"}

def test_ensure_consistent_length_valid():
    sequence_dict = {"Taxon1": "AAA", "Taxon2": "GGG", "Taxon3": "TTT"}
    ensure_consistent_length(sequence_dict)  # should not raise

def test_ensure_consistent_length_invalid():
    sequence_dict = {"Taxon1": "AAA", "Taxon2": "GG", "Taxon3": "TTT"}
    try:
        ensure_consistent_length(sequence_dict)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "Inconsistent sequence lengths" in str(e)

if __name__ == "__main__":
    test_pad_sequence()
    test_get_all_taxa()
    test_ensure_consistent_length_valid()
    test_ensure_consistent_length_invalid()
    print("sequence_utils passed ✔️")