#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List

from mips_sim import run_sim


class MipsGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MIPS32 Simulator")
        self.root.geometry("900x600")

        self._build_ui()

    def _build_ui(self) -> None:
        top = tk.Frame(self.root)
        top.pack(fill=tk.X, padx=10, pady=10)

        self.path_var = tk.StringVar()

        tk.Label(top, text="Input File:").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.path_var, width=60).pack(side=tk.LEFT, padx=8)
        tk.Button(top, text="Browse", command=self._browse).pack(side=tk.LEFT)
        tk.Button(top, text="Run", command=self._run).pack(side=tk.LEFT, padx=8)

        body = tk.Frame(self.root)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text = tk.Text(body, font=("Courier New", 11))
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, "Load a hex input file and click Run.\n")

    def _browse(self) -> None:
        path = filedialog.askopenfilename(
            title="Select hex input file",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if path:
            self.path_var.set(path)

    def _run(self) -> None:
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("Error", "Please select an input file.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            regs = run_sim(lines)
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))
            return

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "Final register values:\n")
        for i, v in enumerate(regs):
            self.text.insert(tk.END, f"R{i:02d} = {v}\n")


def main() -> int:
    root = tk.Tk()
    app = MipsGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
