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
from sequence_concatenator.writers.report_writer import write_report
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
    parser = argparse.ArgumentParser(
        description="Concatenate aligned biological sequences and generate report."
    )
    parser.add_argument(
        "input_files", nargs="+", help="Paths to input sequence files"
    )
    parser.add_argument(
        "--out", required=True, help="Base name for output files (no extension)"
    )
    parser.add_argument(
        "--missing", default="?", help="Missing data character (default: ? )"
    )
    parser.add_argument(
        "--nexus", action="store_true", help="Also export NEXUS file"
    )
    parser.add_argument(
        "--pdf", action="store_true", help="Generate a PDF report"
    )
    args = parser.parse_args()

    # Read inputs
    sequence_dicts = []
    for path in args.input_files:
        print(f"Reading: {path}")
        sequence_dicts.append(read_file_auto(path))

    # Merge sequences
    merged, partitions = merge_sequences(
        sequence_dicts, placeholder=args.missing
    )

    # Write FASTA
    fasta_path = args.out + ".fasta"
    write_fasta(merged, fasta_path)

    # Partition file
    partition_txt = args.out + "_partition.txt"
    partition_text = generate_partition_file(partitions, codon=True)
    write_partition_file(partition_text, partition_txt)

    # NEXUS (optional)
    if args.nexus:
        nexus_path = args.out + ".nex"
        write_nexus(merged, nexus_path, partition_text)

    # Statistics
    stats = compute_alignment_stats(merged, missing_char=args.missing)
    print("\nAlignment Summary:")
    print(f"- Taxa: {stats['num_taxa']}")
    print(f"- Length: {stats['alignment_length']} bp")
    print(f"- Missing: {stats['missing_count']} ({stats['missing_percentage']}%)")

    # Report (PDF)
    if args.pdf:
        report_path = args.out + ".pdf"
        write_report(merged, partitions, stats, args.input_files, report_path)
        print(f"PDF report written to: {report_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()