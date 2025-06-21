from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
from pathlib import Path

def write_fasta(sequence_dict, output_path):
    """
    Writes concatenated sequences to a FASTA file.

    Args:
        sequence_dict (dict): {taxon: sequence}
        output_path (str): Output FASTA file path
    """
   # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    

    records = []
    for taxon, sequence in sequence_dict.items():
        record = SeqRecord(Seq(sequence), id=taxon, description="")
        records.append(record)

    SeqIO.write(records, output_path, "fasta")