from input.fasta_reader import read_fasta
from input.nexus_reader import read_nexus
from input.genbank_reader import read_genbank

def test_fasta_reader():
    data = read_fasta("../test_data/test1.fasta")
    assert isinstance(data, dict)
    assert len(data) > 0
    print("FASTA reader passed ✔️")

def test_nexus_reader():
    data = read_nexus("../test_data/test2.nex")
    assert isinstance(data, dict)
    assert len(data) > 0
    print("NEXUS reader passed ✔️")

def test_genbank_reader():
    data = read_genbank("../test_data/test3.gbff")
    assert isinstance(data, dict)
    assert len(data) > 0
    print("GenBank reader passed ✔️")

if __name__ == "__main__":
    test_fasta_reader()
    test_nexus_reader()
    test_genbank_reader()
