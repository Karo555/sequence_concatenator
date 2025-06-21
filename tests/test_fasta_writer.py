import os
from export.fasta_writer import write_fasta
from Bio import SeqIO

def test_write_fasta():
    test_data = {
        "Taxon1": "AAAGGG",
        "Taxon2": "CCCTTT"
    }

    output_file = "test_data/output_test.fasta"
    write_fasta(test_data, output_file)

    # Read back and check contents
    records = list(SeqIO.parse(output_file, "fasta"))
    assert len(records) == 2
    assert records[0].id == "Taxon1"
    assert str(records[0].seq) == "AAAGGG"
    assert records[1].id == "Taxon2"
    assert str(records[1].seq) == "CCCTTT"

    print("fasta_writer passed ✔️")

    # Cleanup
    os.remove(output_file)

if __name__ == "__main__":
    test_write_fasta()