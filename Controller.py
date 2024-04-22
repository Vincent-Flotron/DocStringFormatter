from View import View
from Doc_String import Doc_String
from File_Manager import File_Manager
from Config import Config

class Controller:

    def __init__( self ):
        self._name    = 'controller'
        self._view    = View( self )
        self._config  = Config( self )
        self._doc_str = Doc_String( self._view, self._config )

    def edit_setting( self, setting_section, setting_name ):
        previous_value = self._config.get_setting(setting_section, setting_name)
        # Prompt the user to enter the default text editor
        text_editor = self._view.ask_for( f"Enter new {setting_name} [{previous_value}] (leave empty to keep current): " ).strip()
        if text_editor != '':
            status_message = self._config.edit_setting( setting_section, setting_name, text_editor )
            self._view.display(status_message)

    def edit_comment_start(self):
        self._config.edit_comment_start()

    def edit_comment_end(self):
        self._config.edit_comment_end()

    def edit_nb_indentation(self):
        self._config.edit_nb_indentation()

    def edit_default_editor( self ):
        self._config.edit_default_editor()


    # def edit_default_editor( self ):
    #     previous_text_editor = self._config.get_default_editor()
    #     # Prompt the user to enter the default text editor
    #     text_editor = self._view.ask_for( f"Enter the default text editor [{previous_text_editor}] (leave empty to keep current): " ).strip()
    #     status_message = self._config.edit_default_editor( text_editor )
    #     self._view.display(status_message)

    # on click button
    # def generate_doc_string( self ):
    #     method_declaration = self._view.get_method_declaration()
        
    #     parameters = self._doc_str.extract_parameters( method_declaration )


        # description        = description_entry.get("1.0", tk.END).strip()
        # notes = notes_entry.get("1.0", tk.END).strip()
        # examples = examples_entry.get("1.0", tk.END).strip()

        # template_file = "template.txt"  # Change this to your template file path
        # template = read_template_from_file(template_file)
        
        # filled_template = fill_template(template, description, notes, parameters, examples)
        
        # formatted_documentation_text.delete("1.0", tk.END)
        # formatted_documentation_text.insert("1.0", filled_template)

    def generate_doc_string( self ):
        self.update_model()
        self._doc_str.generate_doc_string()
        View.update_text(self._view.formatted_documentation_text, self._doc_str.get_doc_string())
        print('################ GENERATED DOC STRING #################')
        print( self._doc_str.get_doc_string() )
    
    def update_model( self ):
        text_inputs = self._view.get_text_inputs()
        for key, text_input in text_inputs.items():
            if text_input.is_parameter():
                self._doc_str.update_parameter( text_input.get_name(), text_input.get_text() )
            else:
                self._doc_str.update_section( text_input.get_name(), text_input.get_text() )

    def extract_parameters( self, method_declaration ):
        self._view.clear_parameters_frame()
        self._doc_str.extract_parameters_from_method( method_declaration )

        # Update view
        self._view.display_sections( self._doc_str.get_sections() ) 
        

    def run( self ):
        # vars = self._doc_str.get_sections()

        # for key, var in vars.items():
        #     print( var.get_name() )
        #     print( f'{var.get_position().get_start()} {var.get_position().get_end()}')
        #     print( var.get_text() )
        #     print( var.get_offset())
        #     print('----------')

        # self._doc_str.count_width()
        # print (f'width: {self._doc_str._width}')

        # note_text = """Note:
        # This is a note.
        # And this note is very nice.
        #     Could you see it ?"""

        # note_parameter = """Parameter:
        # This is a parameter.
        # And this parameter is very nice.
        #     Could you see it ?"""

        # note_example = """Example:
        # This is a Example.
        # And this Example is very nice.
        #     Could you see it ?"""

        # note_description = """Description:
        # This is a description.
        # And this description is very nice.
        #     Could you see it ?"""

        # self._doc_str.update_section('Notes', note_text)
        # self._doc_str.update_section('Parameters', note_parameter)
        # self._doc_str.update_section('Examples', note_example)
        # self._doc_str.update_section('Description', note_description)

        # self._doc_str.generate_doc_string()

        # print(self._doc_str.get_doc_string())

        self._view.endless_loop()

    def edit_template( self ):
        if not File_Manager.open_file_with_text_editor('template.txt', self._config.get_default_editor()):
            controller._view.display("Unable to determine default text editor.")

# MAIN ---------------------------------------------------------------------------- #
if __name__ == "__main__":

    controller = Controller()
    controller.run()