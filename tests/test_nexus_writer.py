# test_nexus_writer.py

import os
from export.nexus_writer import write_nexus
from pathlib import Path

def test_write_nexus():
    os.makedirs("test_data", exist_ok=True)

    sequence_dict = {
        "Taxon1": "AAAGGG",
        "Taxon2": "CCCTTT"
    }

    partition_text = """
CHARSET gene1 = 1-3;
CHARSET gene2 = 4-6;
"""

    output_file = "test_data/output_test.nex"
    write_nexus(sequence_dict, output_file, partition_text)

    assert Path(output_file).exists(), "Output file was not created"

    with open(output_file, "r") as f:
        content = f.read()
        assert "#NEXUS" in content
        assert "Matrix" in content
        assert "CHARSET gene1" in content

    print("nexus_writer passed ✔️")

    # os.remove(output_file)

if __name__ == "__main__":
    test_write_nexus()