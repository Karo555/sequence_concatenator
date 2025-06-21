from pathlib import Path

def get_extension(path):
    """
    Returns the lowercase file extension without the leading dot.

    Args:
        path (str or Path): File path

    Returns:
        str: e.g. "fasta", "nex", "gbff"
    """
    return Path(path).suffix.lower().lstrip(".")

def is_supported_format(path):
    """
    Checks if the file has a supported sequence format.

    Args:
        path (str or Path): File path

    Returns:
        bool: True if extension is recognized
    """
    return get_extension(path) in {"fasta", "fa", "nex", "gbff"}

def group_files_by_type(paths):
    """
    Groups a list of paths by their file format.

    Args:
        paths (list of str or Path): List of file paths

    Returns:
        dict: {ext: [path1, path2, ...]}
    """
    grouped = {}
    for path in paths:
        ext = get_extension(path)
        grouped.setdefault(ext, []).append(path)
    return grouped