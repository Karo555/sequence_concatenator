import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class SequenceViewer(tk.Toplevel):
    def __init__(self, parent, sequences, on_update=None):
        """
        Sequence editor/viewer window.

        Args:
            parent (tk.Tk): Parent window
            sequences (dict): {taxon: sequence}
            on_update (callable, optional): Callback function to receive updated sequences
        """
        super().__init__(parent)
        self.title("Sequence Editor")
        self.geometry("800x500")

        self.original_sequences = sequences
        self.sequences = sequences.copy()
        self.on_update = on_update
        self.current_taxon = None

        self._build_ui()
        self._load_taxa()
        self._show_all_sequences()

    def _build_ui(self):
        # Left panel: taxa list and controls
        taxa_frame = tk.Frame(self)
        taxa_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.taxa_list = tk.Listbox(taxa_frame, height=20)
        self.taxa_list.pack(fill=tk.Y, expand=True)

        button_frame = tk.Frame(taxa_frame)
        button_frame.pack(fill=tk.X, pady=5)

        tk.Button(button_frame, text="View", command=self._view_selected).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Rename", command=self._rename_selected).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Remove", command=self._remove_selected).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Apply Edit", command=self._apply_edit).pack(fill=tk.X, pady=2)
        tk.Button(button_frame, text="Save Changes", command=self._save_changes).pack(fill=tk.X, pady=10)

        # Right panel: sequence display/edit area
        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Courier", 10))
        self.text_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_box.config(state=tk.DISABLED)

    def _load_taxa(self):
        self.taxa_list.delete(0, tk.END)
        for taxon in sorted(self.sequences.keys()):
            self.taxa_list.insert(tk.END, taxon)

    def _show_all_sequences(self):
        """
        Display all sequences read-only in FASTA style.
        """
        self.current_taxon = None
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        for taxon, seq in self.sequences.items():
            self.text_box.insert(tk.END, f">{taxon}\n")
            for i in range(0, len(seq), 80):
                self.text_box.insert(tk.END, seq[i:i+80] + "\n")
            self.text_box.insert(tk.END, "\n")
        self.text_box.config(state=tk.DISABLED)

    def _view_selected(self):
        """
        Display only the selected taxon's sequence and enable editing.
        """
        selection = self.taxa_list.curselection()
        if not selection:
            return
        taxon = self.taxa_list.get(selection[0])
        self.current_taxon = taxon
        seq = self.sequences.get(taxon, "")

        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, f">{taxon}\n")
        for i in range(0, len(seq), 80):
            self.text_box.insert(tk.END, seq[i:i+80] + "\n")
        self.text_box.config(state=tk.NORMAL)

    def _rename_selected(self):
        selection = self.taxa_list.curselection()
        if not selection:
            return
        old_name = self.taxa_list.get(selection[0])
        new_name = simpledialog.askstring("Rename Taxon", f"Enter new name for '{old_name}':", initialvalue=old_name)
        if new_name and new_name != old_name:
            self.sequences[new_name] = self.sequences.pop(old_name)
            self._load_taxa()
            self._show_all_sequences()
            messagebox.showinfo("Renamed", f"'{old_name}' renamed to '{new_name}'")

    def _remove_selected(self):
        selection = self.taxa_list.curselection()
        if not selection:
            return
        taxon = self.taxa_list.get(selection[0])
        if messagebox.askyesno("Remove Taxon", f"Remove '{taxon}'?"):
            del self.sequences[taxon]
            self._load_taxa()
            self._show_all_sequences()

    def _apply_edit(self):
        """
        Apply changes made in the text box to the current taxon's sequence.
        """
        if not self.current_taxon:
            messagebox.showwarning("No Taxon Selected", "Select a taxon and click View to edit its sequence.")
            return
        content = self.text_box.get(1.0, tk.END).strip().splitlines()
        if not content or not content[0].startswith('>'):
            messagebox.showerror("Invalid Format", "Sequence must start with '>' followed by taxon name.")
            return
        # Skip header line
        seq_lines = content[1:]
        new_seq = ''.join(line.strip() for line in seq_lines)
        self.sequences[self.current_taxon] = new_seq
        messagebox.showinfo("Sequence Updated", f"Sequence for '{self.current_taxon}' has been updated.")

    def _save_changes(self):
        """
        Trigger the update callback with modified sequences.
        """
        if self.on_update:
            self.on_update(self.sequences)
        self.destroy()