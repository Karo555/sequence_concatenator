def compute_alignment_stats(sequence_dict, missing_char="?"):
    """
    Computes basic statistics from a concatenated sequence alignment.

    Args:
        sequence_dict (dict): {taxon: sequence}
        missing_char (str): Character used for missing data ("?" or "-")

    Returns:
        dict: {
            "num_taxa": int,
            "alignment_length": int,
            "missing_count": int,
            "missing_percentage": float
        }
    """
    if not sequence_dict:
        return {
            "num_taxa": 0,
            "alignment_length": 0,
            "missing_count": 0,
            "missing_percentage": 0.0
        }

    num_taxa = len(sequence_dict)
    alignment_length = len(next(iter(sequence_dict.values())))
    total_positions = num_taxa * alignment_length

    missing_count = sum(seq.count(missing_char) for seq in sequence_dict.values())
    missing_percentage = round((missing_count / total_positions) * 100, 2)

    return {
        "num_taxa": num_taxa,
        "alignment_length": alignment_length,
        "missing_count": missing_count,
        "missing_percentage": missing_percentage
    }