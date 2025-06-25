import os
import tempfile
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt


def write_report(merged, partitions, stats, input_files, output_path):
    """
    Writes a PDF report summarizing the concatenation run with charts.

    Args:
        merged (dict): {taxon: concatenated_sequence}
        partitions (list): [(gene_label, start, end), ...]
        stats (dict): Alignment statistics from compute_alignment_stats
        input_files (list): List of input file paths
        output_path (str): Path to write the PDF report
    """
    # Ensure output directory exists
    directory = os.path.dirname(output_path) or '.'
    os.makedirs(directory, exist_ok=True)

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Initialize PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Sequence Concatenator Report", ln=True, align="C")
    pdf.ln(5)

    # Timestamp
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Generated: {now}", ln=True)
    pdf.ln(5)

    # Input files
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Input Files:", ln=True)
    pdf.set_font("Arial", '', 12)
    for path in input_files:
        pdf.cell(0, 6, f"- {os.path.basename(path)}", ln=True)
    pdf.ln(5)

    # Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Summary:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 6, f"Taxa: {stats.get('num_taxa', 0)}", ln=True)
    pdf.cell(0, 6, f"Alignment length: {stats.get('alignment_length', 0)} bp", ln=True)
    pdf.cell(0, 6, f"Missing data: {stats.get('missing_count', 0)} ({stats.get('missing_percentage', 0)}%)", ln=True)
    pdf.ln(5)

    # Partition info text
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Partitions:", ln=True)
    pdf.set_font("Arial", '', 12)
    for label, start, end in partitions:
        pdf.cell(0, 6, f"- {label}: {start}-{end}", ln=True)
    pdf.ln(5)

    # Generate charts
    # 1) Missing data per taxon
    taxa = list(merged.keys())
    missing_pct = [round((seq.count('?')/len(seq))*100, 2) if len(seq)>0 else 0 for seq in merged.values()]
    fig, ax = plt.subplots()
    ax.bar(taxa, missing_pct)
    ax.set_ylabel('Missing Data (%)')
    ax.set_title('Missing Data per Taxon')
    chart1 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(chart1.name, bbox_inches='tight')
    plt.close(fig)
    pdf.image(chart1.name, w=180)
    os.unlink(chart1.name)
    pdf.ln(5)

    # 2) Partition lengths
    labels = [p[0] for p in partitions]
    lengths = [p[2] - p[1] + 1 for p in partitions]
    fig, ax = plt.subplots()
    ax.bar(labels, lengths)
    ax.set_ylabel('Length (bp)')
    ax.set_title('Partition Lengths')
    chart2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(chart2.name, bbox_inches='tight')
    plt.close(fig)
    pdf.image(chart2.name, w=180)
    os.unlink(chart2.name)

    # Save PDF
    pdf.output(output_path)