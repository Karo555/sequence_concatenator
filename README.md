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

## license
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Karo555/sequence_concatenator/LICENSE) file for details. <br>