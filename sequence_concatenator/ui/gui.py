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
import os
from sequence_concatenator.core.stats import compute_alignment_stats
from sequence_concatenator.ui.viewer import SequenceViewer

class SequenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sequence Concatenator")
        self.sequence_dicts = []
        self.loaded_files = []  # Track loaded file paths

        self.build_interface()

    def build_interface(self):
        # Button frame for horizontal layout
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.select_button = tk.Button(button_frame, text="Select Sequence Files", command=self.load_files)
        self.select_button.pack(side="left", padx=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side="left", padx=5)

        # File list frame
        files_frame = tk.Frame(self.root)
        files_frame.pack(pady=10, fill='both', expand=True)
        
        tk.Label(files_frame, text="Loaded Files:", font=("Arial", 10, "bold")).pack(anchor='w')
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(files_frame)
        listbox_frame.pack(fill='both', expand=True)
        
        self.files_listbox = tk.Listbox(listbox_frame, height=6)
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.run_button = tk.Button(self.root, text="Concatenate and Export", command=self.run_pipeline)
        self.run_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="Ready", fg="green", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(pady=5, fill='x', padx=20)

        self.stats_text = tk.Text(self.root, height=12, width=60)
        self.stats_text.pack(pady=10)

    def remove_selected_file(self):
        """Remove the selected file from the loaded files list"""
        selection = self.files_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file to remove.")
            return
        
        # Get the selected index
        selected_index = selection[0]
        
        # Remove from both lists
        removed_file = os.path.basename(self.loaded_files[selected_index])
        del self.sequence_dicts[selected_index]
        del self.loaded_files[selected_index]
        
        # Update display
        self.update_files_display()
        self.status_label.config(text=f"Removed: {removed_file}", fg="blue")
        
        # Clear stats if no files left
        if not self.loaded_files:
            self.stats_text.delete(1.0, tk.END)

    def update_status(self, message, is_working=False):
        """Update status label and progress bar"""
        self.status_label.config(text=message, fg="blue" if is_working else "green")
        if is_working:
            self.progress.start(10)
        else:
            self.progress.stop()
        self.root.update()

    def update_files_display(self):
        """Update the files listbox with loaded files"""
        self.files_listbox.delete(0, tk.END)
        for i, file_path in enumerate(self.loaded_files):
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, f"{i+1}. {filename}")

    def clear_all(self):
        """Clear all loaded files and reset the interface"""
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

        for i, path in enumerate(paths):
            if path in self.loaded_files:
                continue  # Skip already loaded files

            self.update_status(f"Loading file {i+1}/{len(paths)}: {os.path.basename(path)}", True)
            ext = os.path.splitext(path)[1].lower()

            try:
                if ext in [".fasta", ".fa"]:
                    self.sequence_dicts.append(read_fasta(path))
                elif ext == ".nex":
                    self.sequence_dicts.append(read_nexus(path))
                elif ext == ".gbff":
                    self.sequence_dicts.append(read_genbank(path))
                else:
                    continue  # Skip unsupported file
                self.loaded_files.append(path)
            except Exception as e:
                self.update_status("Error loading files", False)
                messagebox.showerror("Read Error", f"Failed to read {path}:\n{e}")
                return

        self.update_files_display()
        self.update_status(f"Loaded {len(self.sequence_dicts)} file(s) successfully", False)
        messagebox.showinfo("Files Loaded", f"Total loaded: {len(self.sequence_dicts)}.")


    def run_pipeline(self):
        if not self.sequence_dicts:
            messagebox.showwarning("No Data", "Please load sequence files first.")
            return

        self.update_status("Merging sequences...", True)
        merged, partitions = merge_sequences(self.sequence_dicts, placeholder="?")

        # Ask for output base path
        output_base = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("FASTA", "*.fasta")])
        if not output_base:
            self.update_status("Export cancelled", False)
            return

        fasta_path = output_base
        partition_path = output_base.replace(".fasta", "_partition.txt")
        nexus_path = output_base.replace(".fasta", ".nex")

        self.update_status("Writing FASTA file...", True)
        write_fasta(merged, fasta_path)

        self.update_status("Generating partition file...", True)
        partition_text = generate_partition_file(partitions, codon=True)
        write_partition_file(partition_text, partition_path)
        
        self.update_status("Writing NEXUS file...", True)
        write_nexus(merged, nexus_path, partition_text)
        
        self.update_status("Opening sequence viewer...", True)
        SequenceViewer(self.root, merged)
        
        self.update_status("Computing statistics...", True)
        # Show stats
        stats = compute_alignment_stats(merged, missing_char="?")

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Taxa: {stats['num_taxa']}\n")
        self.stats_text.insert(tk.END, f"Total alignment length: {stats['alignment_length']} bp\n")
        self.stats_text.insert(tk.END, f"Missing data: {stats['missing_count']} ({stats['missing_percentage']}%)\n")
        self.stats_text.insert(tk.END, f"Output:\n- {os.path.basename(fasta_path)}\n- {os.path.basename(nexus_path)}\n- {os.path.basename(partition_path)}")

        self.update_status("Process completed successfully", False)
        messagebox.showinfo("Done", "Sequence concatenation and export completed!")