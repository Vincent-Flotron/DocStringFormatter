import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re

def read_template_from_file(template_file):
    try:
        with open(template_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("Template file not found!")
        return ""

def fill_template(template, description, notes, parameters, examples):
    filled_template = template.replace("$Description = ''", description)
    filled_template = filled_template.replace("$Notes = ''", notes)
    filled_template = filled_template.replace("$Parameters = '<none>'", parameters)
    filled_template = filled_template.replace("$Examples = ''", examples)
    return filled_template

def extract_parameters(method_declaration):
    regex = re.compile(r"(input|input-output|output|)\s*([\w|-]+)\s+as\s+([\w|-]+)")
    matches = regex.findall(method_declaration)
    parameters = ""
    for io, param, par_type in matches:
        io = io.strip()
        param = param.strip()
        par_type = par_type.strip()
        return_txt = "returns" if io == "output" else ""
        parameters += f"{param} =\n{return_txt} ({par_type})\n"
    return parameters

def format_method_documentation():
    method_declaration = method_declaration_entry.get("1.0", tk.END).strip()
    description = description_entry.get("1.0", tk.END).strip()
    notes = notes_entry.get("1.0", tk.END).strip()
    examples = examples_entry.get("1.0", tk.END).strip()
    
    parameters = extract_parameters(method_declaration)
    template_file = "template.txt"  # Change this to your template file path
    template = read_template_from_file(template_file)
    
    filled_template = fill_template(template, description, notes, parameters, examples)
    
    formatted_documentation_text.delete("1.0", tk.END)
    formatted_documentation_text.insert("1.0", filled_template)

root = tk.Tk()
root.title("Method Documentation Formatter")

method_declaration_label = tk.Label(root, text="Enter method declaration:")
method_declaration_label.pack()
method_declaration_entry = ScrolledText(root, height=5, width=50)
method_declaration_entry.pack()

description_label = tk.Label(root, text="Enter description:")
description_label.pack()
description_entry = ScrolledText(root, height=2, width=50)
description_entry.pack()

notes_label = tk.Label(root, text="Enter notes:")
notes_label.pack()
notes_entry = ScrolledText(root, height=2, width=50)
notes_entry.pack()

examples_label = tk.Label(root, text="Enter examples:")
examples_label.pack()
examples_entry = ScrolledText(root, height=2, width=50)
examples_entry.pack()

parameters_frame = tk.Frame(root)
parameters_frame.pack()

def add_parameter_entry(param_name):
    param_label = tk.Label(parameters_frame, text=f"{param_name} =")
    param_label.grid(sticky="w")
    param_entry = ScrolledText(parameters_frame, height=2, width=50)
    param_entry.grid(sticky="w")
    return param_entry

def clear_parameters_frame():
    for widget in parameters_frame.winfo_children():
        widget.destroy()

def update_parameters(method_declaration):
    clear_parameters_frame()
    parameters = extract_parameters(method_declaration)
    param_entries = []
    for param_name in parameters.split("\n\n"):
        if param_name.strip():
            param_entry = add_parameter_entry(param_name.strip())
            param_entries.append(param_entry)
    return param_entries

def on_method_declaration_change(event):
    method_declaration = method_declaration_entry.get("1.0", tk.END).strip()
    update_parameters(method_declaration)

method_declaration_entry.bind("<<Modified>>", on_method_declaration_change)

format_button = tk.Button(root, text="Format Documentation", command=format_method_documentation)
format_button.pack()

formatted_documentation_label = tk.Label(root, text="Formatted Documentation:")
formatted_documentation_label.pack()
formatted_documentation_text = ScrolledText(root, height=10, width=50)
formatted_documentation_text.pack()

root.mainloop()
