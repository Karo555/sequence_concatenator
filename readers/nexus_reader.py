from Bio.Nexus import Nexus

def read_nexus(file_path):
    """
    Reads aligned sequences from a NEXUS file.

    Args:
        file_path (str): Path to the NEXUS file.

    Returns:
        dict: A dictionary where keys are taxa names and values are sequences (as strings).
    """
    try:
        nexus_obj = Nexus.Nexus()
        nexus_obj.read(file_path)
        
        sequences = {
            taxon: ''.join(nexus_obj.matrix[taxon])
            for taxon in nexus_obj.matrix
        }
        
        return sequences

    except Exception as e:
        raise IOError(f"Failed to parse NEXUS file '{file_path}': {e}")
