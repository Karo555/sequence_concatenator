from collections import defaultdict
from sequence_concatenator.utils.sequence_utils import get_all_taxa, pad_sequence

def merge_sequences(sequence_dicts, placeholder="?"):
    """
    Concatenates sequences across multiple input sources, aligning by taxon name.

    Args:
        sequence_dicts (list of dict): List of dictionaries [{taxon: sequence}, ...]
        placeholder (str): Placeholder for missing data (e.g., "?" or "-")

    Returns:
        tuple:
            - dict: {taxon: concatenated_sequence}
            - list: list of (gene_label, start, end) tuples for partition info
    """
    all_taxa = get_all_taxa(sequence_dicts)
    merged = defaultdict(str)
    partitions = []

    start = 1
    for idx, seq_dict in enumerate(sequence_dicts):
        gene_len = max(len(seq) for seq in seq_dict.values()) if seq_dict else 0
        end = start + gene_len - 1
        label = f"gene{idx+1}"

        for taxon in all_taxa:
            seq = seq_dict.get(taxon, "")
            padded_seq = pad_sequence(seq, gene_len, filler=placeholder)
            merged[taxon] += padded_seq

        partitions.append((label, start, end))
        start = end + 1

    return dict(merged), partitions