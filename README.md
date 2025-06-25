# sequence_concatenator
## Pre-requirements
Python 3.12+ and [UV](https://github.com/astral-sh/uv) as package manager <br>

## installation 
`git clone https://github.com/Karo555/sequence_concatenator` <br>

## setup virtual env
`uv sync` <br>
`source .venv/bin/activate` <br>

## install in development mode
`uv pip install -e .` <br>

## usage

# CLI
sequencecat input1.fasta input2.nex input3.gbff --out output/combined --nexus
Arguments:

--out: Base path for output files (no extension)
--nexus: Optional; include NEXUS export

# GUI
python main.py
Select input files
Concatenate and export
View aligned sequences and summary statistics

## Supported Formats
Aligned FASTA: .fasta, .fa
Aligned NEXUS: .nex
GenBank: .gbff (uses organism name for taxon label)

## Output Files
The sequence concatenator generates several output files:

### Primary Output Files
- **FASTA file**: Concatenated sequences in FASTA format (.fasta)
- **NEXUS file**: Concatenated sequences with partition information (.nex) - optional
- **Partition file**: RAxML-style partition definition (.txt)

### PDF Report
The tool automatically generates a comprehensive PDF report that includes:

#### Summary Statistics
- Number of taxa processed
- Total alignment length
- Missing data counts and percentages
- List of input files used

#### Visual Charts
- **Missing Data Chart**: Bar chart showing percentage of missing data per taxon
- **Partition Length Chart**: Bar chart displaying the length of each gene partition

#### Partition Information
- Detailed list of all partitions with their start and end positions
- Gene labels and coordinate ranges

The PDF report provides a complete overview of the concatenation process and is useful for quality control and documentation of your phylogenetic analyses.

## license
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Karo555/sequence_concatenator/LICENSE) file for details. <br>