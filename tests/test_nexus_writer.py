import os
from export.nexus_writer import write_nexus
from pathlib import Path

def test_write_nexus():
    sequence_dict = {
        "Taxon1": "AAAGGG",
        "Taxon2": "CCCTTT"
    }

    partition_text = """
CHARSET gene1 = 1-3;
CHARSET gene2 = 4-6;
"""

    output_file = "test_data/output_test.nex"
    
    # Explicitly create the directory
    Path("test_data").mkdir(exist_ok=True)
    print(f"Directory exists: {Path('test_data').exists()}")
    print(f"Current working directory: {os.getcwd()}")
    
    write_nexus(sequence_dict, output_file, partition_text)

    # Verify file exists and content
    assert Path(output_file).exists()

    with open(output_file, "r") as f:
        content = f.read()
        assert "#NEXUS" in content
        assert "Dimensions ntax=2 nchar=6;" in content
        assert "Taxon1" in content
        assert "CHARSET gene1 = 1-3;" in content
        assert "Begin assumptions;" in content

    print("nexus_writer passed ✔️")

    # Cleanup
    os.remove(output_file)

if __name__ == "__main__":
    test_write_nexus()