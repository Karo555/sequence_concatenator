def generate_partition_file(partitions, codon=False):
    """
    Generates partition file content for concatenated alignment.

    Args:
        partitions (list of tuples): [(gene_label, start, end), ...]
        codon (bool): If True, also generate codon position CHARSETs (1st, 2nd, 3rd positions)

    Returns:
        str: Partition file content (as a string)
    """
    lines = []

    for label, start, end in partitions:
        lines.append(f"CHARSET {label} = {start}-{end};")

        if codon:
            lines.append(f"CHARSET {label}_pos1 = {start}-{end}\\3;")
            lines.append(f"CHARSET {label}_pos2 = {start+1}-{end}\\3;")
            lines.append(f"CHARSET {label}_pos3 = {start+2}-{end}\\3;")

    return "\n".join(lines)
