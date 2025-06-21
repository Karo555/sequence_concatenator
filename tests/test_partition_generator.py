from core.partition_generator import generate_partition_file

def test_generate_partition_file():
    partitions = [
        ("gene1", 1, 300),
        ("gene2", 301, 600)
    ]

    # Test without codon positions
    output_basic = generate_partition_file(partitions, codon=False)
    assert "CHARSET gene1 = 1-300;" in output_basic
    assert "CHARSET gene1_pos1" not in output_basic

    # Test with codon positions
    output_codon = generate_partition_file(partitions, codon=True)
    assert "CHARSET gene1 = 1-300;" in output_codon
    assert "CHARSET gene1_pos1 = 1-300\\3;" in output_codon
    assert "CHARSET gene1_pos2 = 2-300\\3;" in output_codon
    assert "CHARSET gene1_pos3 = 3-300\\3;" in output_codon

    print("partition_generator passed ✔️")

if __name__ == "__main__":
    test_generate_partition_file()
