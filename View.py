from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class View:

    def __init__(self, controller):
        self._text_inputs = {}
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("Method Documentation Formatter")

        self._content     = ''
        self._old_content = ''


        # Method declaration
        self._method_declaration_label = tk.Label(self._root, text="Enter method declaration:")
        self._method_declaration_label.pack()
        self._method_declaration_entry = ScrolledText(self._root, height=5, width=50)
        self._method_declaration_entry.pack()

        self._parameters_frame = tk.Frame(self._root)
        self._parameters_frame.pack()

        self._method_declaration_entry.bind("<KeyRelease>", self._content_as_changed)
    
        generate_button = tk.Button(self._root, text="Generate Doc String", command=self._controller.generate_doc_string)
        generate_button.pack()

        self.formatted_documentation_label = tk.Label(self._root, text="Formatted Documentation:")
        self.formatted_documentation_label.pack()
        self.formatted_documentation_text = ScrolledText(self._root, height=10, width=50)
        self.formatted_documentation_text.pack()
        
    def get_text_inputs( self ):
        return self._text_inputs

    def endless_loop(self):
        self._root.mainloop()

    def get_method_declaration(self):
        return self._method_declaration_entry.get("1.0", tk.END).strip()
    
    def _content_as_changed(self, event):
        content = ''
        content = self._method_declaration_entry.get("1.0", tk.END).strip()
        if content != self._old_content:
            self._on_method_declaration_change()
        self._old_content = content
    
    def _on_method_declaration_change(self):
        method_declaration = self._method_declaration_entry.get("1.0", tk.END).strip()
        self._controller.extract_parameters(method_declaration)

    def display(self, text):
        print( f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S.%f")}: {text}')

    def display_sections(self, sections):
        self.clear_parameters_frame()
        parameters = None

        for _, section in sections.items():
            parameters = section.get_parameters()
            if parameters:
                parameters_sorted = section.sort_parameters_by_order()
                for _, param in parameters_sorted.items():
                    self.add_text_input( param.get_name(), param.get_text(), self._parameters_frame, True )       
            self.add_text_input( section.get_name(), section.get_text(), self._parameters_frame, False )
    

    def add_text_input(self, name, text, parent, is_parameter):
        self._text_inputs[name] = Text_Input(name, text, parent, is_parameter)

    def clear_parameters_frame(self):
        self._text_inputs = {}

    def update_text(text_element, text):
        text_element.delete("1.0", tk.END)
        text_element.insert("1.0", text)

    def clear_all( self ):
        for widget in self._parameters_frame.winfo_children():
            widget.destroy()


class Text_Input:
    def __init__(self, name, text, parent, is_parameter):
        self._name  = name
        self._text  = text
        self._label = tk.Label(parent, text=f"{name} =")
        self._label.grid(sticky="w")
        self._entry = ScrolledText(parent, height=2, width=50)
        self._entry.grid(sticky="w")
        self._is_parameter = is_parameter

        View.update_text(self._entry, text)

    def get_name(self):
        return self._name
    
    def set_name(self, new_name):
        self._name = new_name
        self._label.config(text=new_name)

    def set_text(self, new_text):
        self._text = new_text
        View.update_text(self._entry, new_text)

    def get_text(self):
        self._text = self._entry.get('1.0', tk.END)
        return self._text
    
    def __del__( self ):
        self._label.grid_forget()
        self._entry.grid_forget()
    
    def is_parameter( self ):
        return self._is_parameter