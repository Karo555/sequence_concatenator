def pad_sequence(sequence, target_length, filler="?"):
    """
    Pads a sequence to the target length with the given filler character.

    Args:
        sequence (str): Original sequence
        target_length (int): Desired length
        filler (str): Padding character

    Returns:
        str: Padded sequence
    """
    padding_needed = target_length - len(sequence)
    return sequence + (filler * padding_needed)


def get_all_taxa(sequence_dicts):
    """
    Collects all unique taxa names across multiple sequence dictionaries.

    Args:
        sequence_dicts (list of dict): [{taxon: seq}, ...]

    Returns:
        set: All unique taxa
    """
    taxa = set()
    for seq_dict in sequence_dicts:
        taxa.update(seq_dict.keys())
    return taxa


def ensure_consistent_length(sequence_dict):
    """
    Validates that all sequences in a dict are of equal length.

    Args:
        sequence_dict (dict): {taxon: sequence}

    Raises:
        ValueError: If sequences have inconsistent lengths
    """
    lengths = {len(seq) for seq in sequence_dict.values()}
    if len(lengths) > 1:
        raise ValueError(f"Inconsistent sequence lengths: {lengths}")