from View import View
from Doc_String import Doc_String




# Sample text
text = '''
/* Description -----------------------------------------------------------*/
/*                                                                        */
/* $Description = 'This is a description'                                 */
/*                                                                        */
/* Notes -----------------------------------------------------------------*/
/*                                                                        */
/* $Notes = ''                                                            */
/*                                                                        */
/* Parameters ------------------------------------------------------------*/
/*                                                                        */
/* $Parameters = '<none>'                                                 */
/*                                                                        */
/* Examples --------------------------------------------------------------*/
/*                                                                        */
/* $Examples = 12                                                         */
/*                                                                        */
/*------------------------------------------------------------------------*/

'''

doc_str = Doc_String(text)

vars = doc_str.get_variables()

for key, var in vars.items():
    print( var.get_name() )
    print( f'{var.get_position().get_start()} {var.get_position().get_end()}')
    print( var.get_value() )
    print( var.get_offset())
    print('----------')

doc_str.count_width()
print (f'width: {doc_str._width}')

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

doc_str.update_variable('Notes', note_text)
doc_str.update_variable('Parameters', note_parameter)
doc_str.update_variable('Examples', note_example)
doc_str.update_variable('Description', note_description)

doc_str.place_values()

print(doc_str.get_doc_string())