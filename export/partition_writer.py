from pathlib import Path

def write_partition_file(partition_text, output_path):
    """
    Writes partition info (CHARSET entries) to a text file.

    Args:
        partition_text (str): Formatted CHARSET data
        output_path (str): Path to output partition file
    """
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, 'w') as f:
            f.write(partition_text.strip() + '\n')
    except Exception as e:
        raise IOError(f"Failed to write partition file '{output_path}': {e}")
