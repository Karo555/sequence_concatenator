import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sequence_concatenator.readers.fasta_reader import read_fasta
from sequence_concatenator.readers.nexus_reader import read_nexus
from sequence_concatenator.readers.genbank_reader import read_genbank
from sequence_concatenator.core.sequence_merger import merge_sequences
from sequence_concatenator.core.partition_generator import generate_partition_file
from sequence_concatenator.writers.fasta_writer import write_fasta
from sequence_concatenator.writers.partition_writer import write_partition_file
from sequence_concatenator.writers.nexus_writer import write_nexus
from sequence_concatenator.core.stats import compute_alignment_stats
from sequence_concatenator.ui.viewer import SequenceViewer
from sequence_concatenator.writers.report_writer import write_report
import os

class SequenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sequence Concatenator")
        self.sequence_dicts = []
        self.loaded_files = []  # Track loaded file paths

        self.build_interface()

    def build_interface(self):
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.select_button = tk.Button(button_frame, text="Select Sequence Files", command=self.load_files)
        self.select_button.pack(side="left", padx=5)

        self.edit_button = tk.Button(button_frame, text="Edit Merged Sequences", command=self.edit_sequences)
        self.edit_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side="left", padx=5)

        # Loaded files list
        files_frame = tk.Frame(self.root)
        files_frame.pack(pady=10, fill='both', expand=True)

        tk.Label(files_frame, text="Loaded Files:", font=("Arial", 10, "bold")).pack(anchor='w')
        listbox_frame = tk.Frame(files_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.files_listbox = tk.Listbox(listbox_frame, height=6)
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=scrollbar.set)

        self.files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Run pipeline button
        self.run_button = tk.Button(self.root, text="Concatenate, Export, and Report", command=self.run_pipeline)
        self.run_button.pack(pady=10)

        # Status and progress
        self.status_label = tk.Label(self.root, text="Ready", fg="green", font=("Arial", 10))
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(pady=5, fill='x', padx=20)

        # Stats and outputs display
        self.stats_text = tk.Text(self.root, height=15, width=60)
        self.stats_text.pack(pady=10)

    def update_status(self, message, is_working=False):
        self.status_label.config(text=message, fg="blue" if is_working else "green")
        if is_working:
            self.progress.start(10)
        else:
            self.progress.stop()
        self.root.update()

    def update_files_display(self):
        self.files_listbox.delete(0, tk.END)
        for i, file_path in enumerate(self.loaded_files):
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, f"{i+1}. {filename}")

    def clear_all(self):
        self.sequence_dicts.clear()
        self.loaded_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.progress.stop()
        self.status_label.config(text="Ready", fg="green")
        messagebox.showinfo("Cleared", "All data has been cleared.")

    def load_files(self):
        paths = filedialog.askopenfilenames(filetypes=[
            ("All supported", "*.fasta *.fa *.nex *.gbff"),
            ("FASTA", "*.fasta *.fa"),
            ("NEXUS", "*.nex"),
            ("GenBank", "*.gbff")
        ])
        if not paths:
            return

        self.update_status("Loading files...", True)
        for path in paths:
            if path in self.loaded_files:
                continue
            ext = os.path.splitext(path)[1].lower()
            self.update_status(f"Loading {os.path.basename(path)}", True)
            try:
                if ext in [".fasta", ".fa"]:
                    self.sequence_dicts.append(read_fasta(path))
                elif ext == ".nex":
                    self.sequence_dicts.append(read_nexus(path))
                elif ext == ".gbff":
                    self.sequence_dicts.append(read_genbank(path))
                else:
                    continue
                self.loaded_files.append(path)
            except Exception as e:
                self.update_status("Error loading files", False)
                messagebox.showerror("Read Error", f"Failed to read {path}:\n{e}")
                return

        self.update_files_display()
        self.update_status(f"Loaded {len(self.sequence_dicts)} files", False)
        messagebox.showinfo("Files Loaded", f"Total loaded: {len(self.sequence_dicts)} files.")

    def edit_sequences(self):
        if not self.sequence_dicts:
            messagebox.showwarning("No Data", "Load files before editing.")
            return
        merged, _ = merge_sequences(self.sequence_dicts, placeholder="?")
        def on_update(updated):
            self.sequence_dicts = [updated]
            messagebox.showinfo("Updated", "Sequences updated for next run.")
        SequenceViewer(self.root, merged, on_update=on_update)

    def run_pipeline(self):
        if not self.sequence_dicts:
            messagebox.showwarning("No Data", "Please load sequence files first.")
            return
        # Merge
        self.update_status("Merging sequences...", True)
        merged, partitions = merge_sequences(self.sequence_dicts, placeholder="?")
        # Export
        output_base = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                   filetypes=[("PDF Report", "*.pdf")])
        if not output_base:
            self.update_status("Export cancelled", False)
            return
        report_path = output_base

        self.update_status("Writing report...", True)
        stats = compute_alignment_stats(merged, missing_char="?")
        write_report(merged, partitions, stats, self.loaded_files, report_path)

        # Also write data files
        fasta_path = report_path.replace(".pdf", ".fasta")
        partition_path = report_path.replace(".pdf", "_partition.txt")
        nexus_path = report_path.replace(".pdf", ".nex")

        self.write_data_files(merged, partitions, report_path)

        # Show stats
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Generated report: {os.path.basename(report_path)}\n")

        self.update_status("Done", False)
        messagebox.showinfo("Completed", "PDF report and data exports finished!")

    def write_data_files(self, merged, partitions, report_path):
        fasta_path = report_path.replace(".pdf", ".fasta")
        partition_path = report_path.replace(".pdf", "_partition.txt")
        nexus_path = report_path.replace(".pdf", ".nex")
        write_fasta(merged, fasta_path)
        partition_text = generate_partition_file(partitions, codon=True)
        write_partition_file(partition_text, partition_path)
        write_nexus(merged, nexus_path, partition_text)