import tkinter as tk
from tkinter import scrolledtext

class SequenceViewer(tk.Toplevel):
    def __init__(self, parent, sequences):
        super().__init__(parent)
        self.title("Sequence Viewer")
        self.geometry("800x500")

        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Courier", 10))
        self.text_box.pack(fill=tk.BOTH, expand=True)

        self.load_sequences(sequences)

    def load_sequences(self, sequences):
        """
        Load sequences into the text box in FASTA-style format.

        Args:
            sequences (dict): {taxon: sequence}
        """
        self.text_box.delete(1.0, tk.END)

        for taxon, seq in sequences.items():
            self.text_box.insert(tk.END, f">{taxon}\n")
            for i in range(0, len(seq), 80):
                self.text_box.insert(tk.END, seq[i:i+80] + "\n")

        self.text_box.config(state=tk.DISABLED)