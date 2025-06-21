from core.sequence_merger import merge_sequences

def test_merge_sequences():
    input_dicts = [
        {"Taxon1": "AAA", "Taxon2": "CCC"},
        {"Taxon1": "GGG", "Taxon3": "TTT"},
        {"Taxon2": "TTT", "Taxon3": "AAA"}
    ]

    merged, partitions = merge_sequences(input_dicts, placeholder="?")

    assert merged["Taxon1"] == "AAAGGG???"
    assert merged["Taxon2"] == "CCC???TTT"
    assert merged["Taxon3"] == "???TTTAAA"

    assert partitions == [
        ("gene1", 1, 3),
        ("gene2", 4, 6),
        ("gene3", 7, 9)
    ]

    print("sequence_merger passed ✔️")

if __name__ == "__main__":
    test_merge_sequences()
