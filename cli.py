import argparse
from sequence_concatenator.readers.fasta_reader import read_fasta
from sequence_concatenator.readers.nexus_reader import read_nexus
from sequence_concatenator.readers.genbank_reader import read_genbank
from sequence_concatenator.core.sequence_merger import merge_sequences
from sequence_concatenator.core.partition_generator import generate_partition_file
from sequence_concatenator.writers.fasta_writer import write_fasta
from sequence_concatenator.writers.nexus_writer import write_nexus
from sequence_concatenator.writers.partition_writer import write_partition_file
from sequence_concatenator.core.stats import compute_alignment_stats
from sequence_concatenator.utils.file_utils import get_extension


from pathlib import Path

def read_file_auto(path):
    ext = get_extension(path)
    if ext in {"fasta", "fa"}:
        return read_fasta(path)
    elif ext == "nex":
        return read_nexus(path)
    elif ext == "gbff":
        return read_genbank(path)
    else:
        raise ValueError(f"Unsupported format: {ext}")

def main():
    parser = argparse.ArgumentParser(description="Concatenate aligned biological sequences from multiple files.")
    parser.add_argument("input_files", nargs="+", help="Paths to input sequence files")
    parser.add_argument("--out", required=True, help="Base name for output files (no extension)")
    parser.add_argument("--missing", default="?", help="Missing data character (default: ?)")
    parser.add_argument("--nexus", action="store_true", help="Also export NEXUS file")

    args = parser.parse_args()

    # Read all inputs
    sequence_dicts = []
    for path in args.input_files:
        print(f"Reading: {path}")
        sequence_dicts.append(read_file_auto(path))

    # Merge
    merged, partitions = merge_sequences(sequence_dicts, placeholder=args.missing)

    # Write FASTA
    write_fasta(merged, args.out + ".fasta")

    # Partition file
    partition_text = generate_partition_file(partitions, codon=True)
    write_partition_file(partition_text, args.out + "_partition.txt")

    # NEXUS (optional)
    if args.nexus:
        write_nexus(merged, args.out + ".nex", partition_text)

    # Stats
    stats = compute_alignment_stats(merged, missing_char=args.missing)
    print("\nAlignment Summary:")
    print(f"- Taxa: {stats['num_taxa']}")
    print(f"- Length: {stats['alignment_length']} bp")
    print(f"- Missing: {stats['missing_count']} ({stats['missing_percentage']}%)")
    print("\nDone.")

if __name__ == "__main__":
    main()