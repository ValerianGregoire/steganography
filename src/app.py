import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Create main application window
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("450x450")
root.resizable(False, False)

# Function for file selection
def select_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Function to execute the write program
def write_steganography():
    input_file = "\"" + write_input_entry.get().strip() + "\""
    output_file = os.path.join(os.path.expanduser("~/Desktop"), write_output_entry.get().strip())
    lsb_value = write_lsb_spinbox.get()
    use_gray = write_gray_var.get()
    no_red = not write_red_var.get()
    no_green = not write_green_var.get()
    no_blue = not write_blue_var.get()

    if not input_file or not output_file:
        messagebox.showerror("Error", "Please provide input and output file names.")
        return

    # Write user text to a file
    textFile = "./tempText.txt"
    with open(textFile, "w") as file:
        file.write(write_text_textbox.get("1.0", tk.END))

    command = f"python ./write.py {input_file} {output_file} -n {lsb_value} -fromfile {textFile}"
    if use_gray:
        command += " -gray"
    if no_red:
        command += " -nored"
    if no_green:
        command += " -nogreen"
    if no_blue:
        command += " -noblue"

    os.system(command)
    messagebox.showinfo("Success", "Steganography writing completed!")

# Function to execute the read program
def read_steganography():
    input_file = read_input_entry.get().strip()
    lsb_value = read_lsb_spinbox.get()
    max_chars = int(read_chars_spinbox.get().strip())
    no_red = not read_red_var.get()
    no_green = not read_green_var.get()
    no_blue = not read_blue_var.get()

    if not input_file:
        messagebox.showerror("Error", "Please provide an input file.")
        return

    output_file = os.path.join(os.path.dirname(input_file), "textOutput.txt")
    command = f'python ./read.py "{input_file}" "{output_file}" -n {lsb_value}'
    if max_chars:
        command += f" -l {max_chars}"
    if no_red:
        command += " -nored"
    if no_green:
        command += " -nogreen"
    if no_blue:
        command += " -noblue"

    os.system(command)

    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            text = "".join([ch for ch in f.read() if ch.isalnum])
            read_output_textbox.delete("1.0", tk.END)
            read_output_textbox.insert(tk.END, text)
        messagebox.showinfo("Success", "Data read successfully!")
    else:
        messagebox.showerror("Error", "No output file generated. Check your input.")

# Function to copy output text to clipboard
def copy_to_clipboard():
    try:
        root.clipboard_clear()
        root.clipboard_append(read_output_textbox.get("1.0", tk.END).strip())
        root.update()  # Update clipboard
        messagebox.showinfo("Info", "Text copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy text to clipboard: {e}")

# Create tabbed interface
notebook = ttk.Notebook(root)

# Tab 1: Write
write_tab = ttk.Frame(notebook)
notebook.add(write_tab, text="Write")

write_input_label = ttk.Label(write_tab, text="Original image path:")
write_input_label.pack(pady=5)
write_input_entry = ttk.Entry(write_tab, width=50)
write_input_entry.pack(pady=5)
ttk.Button(write_tab, text="Select File", command=lambda: select_file(write_input_entry)).pack(pady=5)

write_output_label = ttk.Label(write_tab, text="Modified image name:")
write_output_label.pack(pady=5)
write_output_entry = ttk.Entry(write_tab, width=50)
write_output_entry.pack(pady=5)

write_text_label = ttk.Label(write_tab, text="Text to write (ASCII only):")
write_text_label.pack(pady=5)
write_text_textbox = tk.Text(write_tab, height=5, width=50, state="normal")
write_text_textbox.pack(pady=5)

write_lsb_frame = ttk.Frame(write_tab)
write_lsb_frame.pack(pady=5)
write_lsb_label = ttk.Label(write_lsb_frame, text="Number of LSB:")
write_lsb_label.pack(pady=5, side='left', padx=5)
write_lsb_spinbox = ttk.Spinbox(write_lsb_frame, from_=1, to=8, width=5)
write_lsb_spinbox.set(1)
write_lsb_spinbox.pack(pady=5, side='left', padx=5)

write_check_frame = ttk.Frame(write_tab)
write_check_frame.pack(pady=5)
write_gray_var = tk.BooleanVar(value=False)
write_red_var = tk.BooleanVar(value=True)
write_green_var = tk.BooleanVar(value=True)
write_blue_var = tk.BooleanVar(value=True)

ttk.Checkbutton(write_check_frame, text="Use Grayscale", variable=write_gray_var).pack(side='left', pady=5, padx=5)
ttk.Checkbutton(write_check_frame, text="Keep Red", variable=write_red_var).pack(side='left', pady=5, padx=5)
ttk.Checkbutton(write_check_frame, text="Keep Green", variable=write_green_var).pack(side='left', pady=5, padx=5)
ttk.Checkbutton(write_check_frame, text="Keep Blue", variable=write_blue_var).pack(side='left', pady=5, padx=5)

ttk.Button(write_tab, text="Execute", command=write_steganography).pack(pady=10)

# Tab 2: Read
read_tab = ttk.Frame(notebook)
notebook.add(read_tab, text="Read")

read_input_label = ttk.Label(read_tab, text="Input Image:")
read_input_label.pack(pady=5)
read_input_entry = ttk.Entry(read_tab, width=50)
read_input_entry.pack(pady=5)
ttk.Button(read_tab, text="Select File", command=lambda: select_file(read_input_entry)).pack(pady=5)

read_lsb_frame = ttk.Frame(read_tab)
read_lsb_frame.pack(pady=5)
read_lsb_label = ttk.Label(read_lsb_frame, text="Number of LSB:")
read_lsb_label.pack(side='left', padx=5)
read_lsb_spinbox = ttk.Spinbox(read_lsb_frame, from_=1, to=8, width=5)
read_lsb_spinbox.set(1)
read_lsb_spinbox.pack(side='left', padx=5)
read_chars_label = ttk.Label(read_lsb_frame, text="Max Characters:")
read_chars_label.pack(side='left', padx=5)
read_chars_spinbox = ttk.Spinbox(read_lsb_frame, from_=1, to=float('inf'), width=5)
read_chars_spinbox.set(1)
read_chars_spinbox.pack(side='left', padx=5)

ttk.Label(read_tab, text="Grayscale images are automatically detected as such.").pack()
read_check_frame = ttk.Frame(read_tab)
read_check_frame.pack(pady=5)
read_red_var = tk.BooleanVar(value=True)
read_green_var = tk.BooleanVar(value=True)
read_blue_var = tk.BooleanVar(value=True)

ttk.Checkbutton(read_check_frame, text="Keep Red", variable=read_red_var).pack(side='left', pady=5, padx=5)
ttk.Checkbutton(read_check_frame, text="Keep Green", variable=read_green_var).pack(side='left', pady=5, padx=5)
ttk.Checkbutton(read_check_frame, text="Keep Blue", variable=read_blue_var).pack(side='left', pady=5, padx=5)

read_output_label = ttk.Label(read_tab, text="Extracted Data:")
read_output_label.pack(pady=5)
read_output_textbox = tk.Text(read_tab, height=10, width=50, state="normal")
read_output_textbox.pack(pady=5)

read_buttons_frame = ttk.Frame(read_tab)
read_buttons_frame.pack(pady=5)
ttk.Button(read_buttons_frame, text="Execute", command=read_steganography).pack(anchor='w', side='left', padx=5)
ttk.Button(read_buttons_frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard()).pack(anchor='e',side='left', padx=5)

notebook.pack(expand=True, fill="both")

root.mainloop()
