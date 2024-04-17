from View import View
from Doc_String import Doc_String


class Controller:

    def __init__(self):
        self._name    = 'controller'
        self._view    = View(self)
        self._doc_str = Doc_String(self._view)

    def format_method_documentation(self):
        method_declaration = self._view.get_method_declaration()
        
        parameters = self._doc_str.extract_parameters(method_declaration)


        # description        = description_entry.get("1.0", tk.END).strip()
        # notes = notes_entry.get("1.0", tk.END).strip()
        # examples = examples_entry.get("1.0", tk.END).strip()

        # template_file = "template.txt"  # Change this to your template file path
        # template = read_template_from_file(template_file)
        
        # filled_template = fill_template(template, description, notes, parameters, examples)
        
        # formatted_documentation_text.delete("1.0", tk.END)
        # formatted_documentation_text.insert("1.0", filled_template)

    def update_parameters(self, method_declaration):
        self._view.clear_parameters_frame()
        parameters = self._doc_str.extract_parameters(method_declaration)
        param_entries = []
        for param_name in parameters.split("\n\n"):
            if param_name.strip():
                param_entry = self.view.add_parameter_entry(param_name.strip())
                param_entries.append(param_entry)
        return param_entries
    

    
    def run(self):
        vars = self._doc_str.get_variables()

        for key, var in vars.items():
            print( var.get_name() )
            print( f'{var.get_position().get_start()} {var.get_position().get_end()}')
            print( var.get_value() )
            print( var.get_offset())
            print('----------')

        self._doc_str.count_width()
        print (f'width: {self._doc_str._width}')

        note_text = """Note:
        This is a note.
        And this note is very nice.
            Could you see it ?"""

        note_parameter = """Parameter:
        This is a parameter.
        And this parameter is very nice.
            Could you see it ?"""

        note_example = """Example:
        This is a Example.
        And this Example is very nice.
            Could you see it ?"""

        note_description = """Description:
        This is a description.
        And this description is very nice.
            Could you see it ?"""

        self._doc_str.update_variable('Notes', note_text)
        self._doc_str.update_variable('Parameters', note_parameter)
        self._doc_str.update_variable('Examples', note_example)
        self._doc_str.update_variable('Description', note_description)

        self._doc_str.place_values_into_docstring()

        print(self._doc_str.get_doc_string())

        self._view.endless_loop()


# MAIN ---------------------------------------------------------------------------- #
if __name__ == "__main__":

    controller = Controller()
    controller.run()