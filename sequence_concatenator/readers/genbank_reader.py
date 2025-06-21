from Bio import SeqIO

def read_genbank(file_path):
    """
    Reads aligned sequences from a GenBank (.gbff) file.
    Uses the organism name as the taxon label.

    Args:
        file_path (str): Path to the GenBank file.

    Returns:
        dict: A dictionary where keys are organism names and values are sequences (as strings).
    """
    sequences = {}
    try:
        for record in SeqIO.parse(file_path, "genbank"):
            organism = record.annotations.get("organism", record.id).split()[0]  # Get just "Taxon1"
            sequences[organism] = str(record.seq)
    except Exception as e:
        raise IOError(f"Failed to parse GenBank file '{file_path}': {e}")
    
    return sequences
