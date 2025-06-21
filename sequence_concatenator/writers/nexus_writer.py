from pathlib import Path

def write_nexus(sequence_dict, output_path, partitions=None):
    """
    Writes concatenated sequences to a NEXUS file with optional CHARSET entries.

    Args:
        sequence_dict (dict): {taxon: sequence}
        output_path (str): Output NEXUS file path
        partitions (str, optional): CHARSET text to append (from partition_generator)
    """
    taxa = sorted(sequence_dict.keys())
    alignment_length = len(next(iter(sequence_dict.values())))

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("#NEXUS\n\n")
        f.write("Begin data;\n")
        f.write(f"  Dimensions ntax={len(taxa)} nchar={alignment_length};\n")
        f.write("  Format datatype=dna missing=? gap=-;\n")
        f.write("  Matrix\n")

        for taxon in taxa:
            f.write(f"{taxon:<15} {sequence_dict[taxon]}\n")

        f.write("  ;\nEnd;\n\n")

        if partitions:
            f.write("Begin assumptions;\n")
            f.write(partitions.strip() + '\n')
            f.write("End;\n")
