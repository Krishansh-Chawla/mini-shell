#mini.py  --- a working shell, built from scratch
#standard libraries only: os, shlex, subprocess

import tkinter as tk
from tkinter import scrolledtext
import os                               #talking to the operating system
import shlex                            #splitting lines into words
import subprocess                       #launching other programs
import sys 
import readline
import os
import shlex
import subprocess
import sys


def execute_command(line: str) -> str:
  """Executes a command line and returns the combined stdout/stderr string."""
  argv = shlex.split(line, posix=True)
  if not argv:
    return ""

  if argv[0] == "exit":
    sys.exit(0)

  if argv[0] == "cd":
    try:
      os.chdir(argv[1] if len(argv) > 1 else os.path.expanduser("~"))
      return f"Changed directory to {os.getcwd()}"
    except Exception as e:
      return f"mini: cd: {e}"

  if argv[0] == "pwd":
    return os.getcwd()

  if argv[0] == "echo":
    return " ".join(argv[1:])

  # External commands via subprocess with output capture
  try:
    result = subprocess.run(argv, capture_output=True, text=True, check=False)
    output = ""
    if result.stdout:
      output += result.stdout
    if result.stderr:
      output += result.stderr
    return output.strip()
  except FileNotFoundError:
    return f"mini: command not found: {argv[0]}"
  except Exception as e:
    return f"mini: error: {e}"


class MiniShellGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("Mini Shell GUI")
    self.root.geometry("750x500")

    # Terminal output text area (Dark theme style)
    self.text_area = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff66", insertbackground="white"
    )
    self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=(10, 5))
    self.text_area.config(state=tk.DISABLED)

    # Input frame at the bottom
    input_frame = tk.Frame(root, bg="#1e1e1e")
    input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    prompt_label = tk.Label(
        input_frame, text="mini $ ", bg="#1e1e1e", fg="#00ff66", font=("Courier", 12, "bold")
    )
    prompt_label.pack(side=tk.LEFT)

    self.entry = tk.Entry(
        input_frame,
        bg="#2d2d2d",
        fg="white",
        insertbackground="white",
        font=("Courier", 12),
    )
    self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    self.entry.bind("<Return>", self.on_enter)
    self.entry.focus()

    self.append_output("=== Mini Shell GUI Initialized ===")
    self.append_output("Type commands below (e.g., pwd, ls, python3 nums.py 3)\n")

  def append_output(self, text):
    self.text_area.config(state=tk.NORMAL)
    self.text_area.insert(tk.END, text + "\n")
    self.text_area.config(state=tk.DISABLED)
    self.text_area.see(tk.END)

  def on_enter(self, event):
    line = self.entry.get().strip()
    self.entry.delete(0, tk.END)

    if not line:
      return
    
    self.append_output(f"mini $ {line}")

    if line == "exit":
      self.root.destroy()
      return

    output = execute_command(line)
    if output:
      self.append_output(output)


if __name__ == "__main__":
  root = tk.Tk()
  app = MiniShellGUI(root)
  root.mainloop()