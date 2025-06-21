import tkinter as tk
from tkinter import filedialog, messagebox
from input.fasta_reader import read_fasta
from input.nexus_reader import read_nexus
from input.genbank_reader import read_genbank
from core.sequence_merger import merge_sequences
from core.partition_generator import generate_partition_file
from export.fasta_writer import write_fasta
from export.partition_writer import write_partition_file
from export.nexus_writer import write_nexus
import os
from core.stats import compute_alignment_stats
from ui.viewer import SequenceViewer

class SequenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sequence Concatenator")
        self.sequence_dicts = []

        self.build_interface()

    def build_interface(self):
        self.select_button = tk.Button(self.root, text="Select Sequence Files", command=self.load_files)
        self.select_button.pack(pady=10)

        self.run_button = tk.Button(self.root, text="Concatenate and Export", command=self.run_pipeline)
        self.run_button.pack(pady=10)

        self.stats_text = tk.Text(self.root, height=12, width=60)
        self.stats_text.pack(pady=10)

    def load_files(self):
        paths = filedialog.askopenfilenames(filetypes=[
            ("All supported", "*.fasta *.fa *.nex *.gbff"),
            ("FASTA", "*.fasta *.fa"),
            ("NEXUS", "*.nex"),
            ("GenBank", "*.gbff")
        ])
        self.sequence_dicts.clear()

        for path in paths:
            ext = os.path.splitext(path)[1].lower()
            try:
                if ext in [".fasta", ".fa"]:
                    self.sequence_dicts.append(read_fasta(path))
                elif ext == ".nex":
                    self.sequence_dicts.append(read_nexus(path))
                elif ext == ".gbff":
                    self.sequence_dicts.append(read_genbank(path))
            except Exception as e:
                messagebox.showerror("Read Error", f"Failed to read {path}:\n{e}")
                return

        messagebox.showinfo("Files Loaded", f"Loaded {len(self.sequence_dicts)} files.")

    def run_pipeline(self):
        if not self.sequence_dicts:
            messagebox.showwarning("No Data", "Please load sequence files first.")
            return

        merged, partitions = merge_sequences(self.sequence_dicts, placeholder="?")

        # Ask for output base path
        output_base = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("FASTA", "*.fasta")])
        if not output_base:
            return

        fasta_path = output_base
        partition_path = output_base.replace(".fasta", "_partition.txt")
        nexus_path = output_base.replace(".fasta", ".nex")

        write_fasta(merged, fasta_path)

        partition_text = generate_partition_file(partitions, codon=True)
        write_partition_file(partition_text, partition_path)
        write_nexus(merged, nexus_path, partition_text)
        SequenceViewer(self.root, merged)
        # Show stats
        stats = compute_alignment_stats(merged, missing_char="?")

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Taxa: {stats['num_taxa']}\n")
        self.stats_text.insert(tk.END, f"Total alignment length: {stats['alignment_length']} bp\n")
        self.stats_text.insert(tk.END, f"Missing data: {stats['missing_count']} ({stats['missing_percentage']}%)\n")
        self.stats_text.insert(tk.END, f"Output:\n- {os.path.basename(fasta_path)}\n- {os.path.basename(nexus_path)}\n- {os.path.basename(partition_path)}")

        messagebox.showinfo("Done", "Sequence concatenation and export completed!")