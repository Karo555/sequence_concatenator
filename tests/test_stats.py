from core.stats import compute_alignment_stats

def test_compute_alignment_stats():
    sequences = {
        "Taxon1": "AAAGGG??",
        "Taxon2": "CCC---TT",
        "Taxon3": "GGGAAA--"
    }

    stats = compute_alignment_stats(sequences, missing_char="?")

    assert stats["num_taxa"] == 3
    assert stats["alignment_length"] == 8
    assert stats["missing_count"] == 2  # only "?" are counted
    assert stats["missing_percentage"] == round((2 / (3 * 8)) * 100, 2)

    # test with "-" as missing char
    stats_dash = compute_alignment_stats(sequences, missing_char="-")
    assert stats_dash["missing_count"] == 4
    assert stats_dash["missing_percentage"] == round((4 / 24) * 100, 2)

    print("stats.py passed ✔️")

if __name__ == "__main__":
    test_compute_alignment_stats()
