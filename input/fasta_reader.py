from Bio import SeqIO

def read_fasta(file_path):
    """
    Reads aligned sequences from a FASTA file.

    Args:
        file_path (str): Path to the FASTA file.

    Returns:
        dict: A dictionary where keys are sequence IDs and values are sequences (as strings).
    """
    sequences = {}
    try:
        for record in SeqIO.parse(file_path, "fasta"):
            sequences[record.id] = str(record.seq)
    except Exception as e:
        raise IOError(f"Failed to parse FASTA file '{file_path}': {e}")
    
    return sequences
