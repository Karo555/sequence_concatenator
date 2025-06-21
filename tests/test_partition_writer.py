import os
from export.partition_writer import write_partition_file

def test_write_partition_file():
    partition_text = """
CHARSET gene1 = 1-300;
CHARSET gene2 = 301-600;
CHARSET gene1_pos1 = 1-300\\3;
"""
    output_file = "test_data/output_partition.txt"

    write_partition_file(partition_text, output_file)

    with open(output_file, "r") as f:
        content = f.read()
        assert "CHARSET gene1 = 1-300;" in content
        assert "gene1_pos1" in content

    print("partition_writer passed ✔️")

    # # Cleanup
    # os.remove(output_file)

if __name__ == "__main__":
    test_write_partition_file()