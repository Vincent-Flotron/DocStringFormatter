from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class View:

    def __init__(self, controller):
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("Method Documentation Formatter")
        self.variables = {}


        # Method declaration
        self._method_declaration_label = tk.Label(self._root, text="Enter method declaration:")
        self._method_declaration_label.pack()
        self._method_declaration_entry = ScrolledText(self._root, height=5, width=50)
        self._method_declaration_entry.pack()

        self._parameters_frame = tk.Frame(self._root)
        self._parameters_frame.pack()

        self._method_declaration_entry.bind("<<Modified>>", self._on_method_declaration_change)

        format_button = tk.Button(self._root, text="Format Documentation", command=self._controller.format_method_documentation)
        format_button.pack()

        formatted_documentation_label = tk.Label(self._root, text="Formatted Documentation:")
        formatted_documentation_label.pack()
        formatted_documentation_text = ScrolledText(self._root, height=10, width=50)
        formatted_documentation_text.pack()

        

    def endless_loop(self):
        self._root.mainloop()

    def get_method_declaration(self):
        return self._method_declaration_entry.get("1.0", tk.END).strip()
    
    def _on_method_declaration_change(self, event):
        method_declaration = self._method_declaration_entry.get("1.0", tk.END).strip()
        self._controller.update_parameters(method_declaration)


    def display(self, text):
        print( f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S.%f")}: {text}')

    def add_parameter_entry(self, param_name):
        param_label = tk.Label(self._parameters_frame, text=f"{param_name} =")
        param_label.grid(sticky="w")
        param_entry = ScrolledText(self._parameters_frame, height=2, width=50)
        param_entry.grid(sticky="w")
        return param_entry
    
    def clear_parameters_frame(self):
        for widget in self._parameters_frame.winfo_children():
            widget.destroy()