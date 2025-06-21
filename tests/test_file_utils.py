from utils.file_utils import get_extension, is_supported_format, group_files_by_type

def test_get_extension():
    assert get_extension("test.fasta") == "fasta"
    assert get_extension("file.NEX") == "nex"
    assert get_extension("sample.gbff") == "gbff"
    assert get_extension("weird.name.fa") == "fa"

def test_is_supported_format():
    assert is_supported_format("abc.fasta") is True
    assert is_supported_format("abc.gbff") is True
    assert is_supported_format("abc.nex") is True
    assert is_supported_format("abc.txt") is False

def test_group_files_by_type():
    files = ["a.fasta", "b.fa", "c.nex", "d.gbff", "e.fasta"]
    grouped = group_files_by_type(files)
    assert grouped["fasta"] == ["a.fasta", "e.fasta"]
    assert grouped["fa"] == ["b.fa"]
    assert grouped["nex"] == ["c.nex"]
    assert grouped["gbff"] == ["d.gbff"]

    assert len(grouped) == 4

if __name__ == "__main__":
    test_get_extension()
    test_is_supported_format()
    test_group_files_by_type()
    print("file_utils passed ✔️")
