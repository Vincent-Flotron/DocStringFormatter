import re
from datetime import datetime

class Position:
    def __init__(self, start, end):
        self._start = start
        self._end   = end

    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    

class List_Enhanced(list):
    def most_present_value(self):
        vals_scores = dict()
        
        # Count occurrences of each value in the list
        for val in self:
            score            = vals_scores.get(val, 0) + 1
            vals_scores[val] = score
        
        # Find the value with the highest occurrence
        score_max = 0
        val_most_present = None
        for val, score in vals_scores.items():
            if score > score_max:
                score_max = score
                val_most_present = val

        return val_most_present
    
class String_Enhanced(str):
    def replace_by_position(self, start_pos, end_pos, replacement_string):
        repl = String_Enhanced(self[:start_pos] + replacement_string + self[end_pos:])
        return repl


class Variable:
    def __init__(self, name, value, position, offset, line_position):
        self._name     = name
        self._value    = value
        self._position = position
        self._offset   = offset
        self._text     = ''
        self._line_pos = line_position

    def get_name(self):
        return self._name
    
    def get_value(self):
        return self._value
    
    def get_position(self):
        return self._position
    
    def get_offset(self):
        return self._offset
    
    def set_text(self, text):
        self._text = text
    
    def get_lines(self):
        return re.split(r'\r?\n', self._text)
    
    def get_line_pos(self):
        return self._line_pos
    

class Var_Adapter:
    def adapt_to_str(string_value, decimal_value):
        if string_value != None:
            return string_value
        elif decimal_value != None:
            return str(decimal_value)
        else:
            return ''
        

class Doc_String:
    var_pat   = r'\$(?P<variable>[\w|-|_]+)[ |\t]*=[ |\t]*([\'|"](?P<value_str>(?!\")(?!\').*)?[\'|"]|(?P<value_dec>\d+|\d*\.\d+|\d+\.\d*))'
    width_pat = r'(?<=/\*).*(?=\*/)'
    com_pat   = r'(?<=/\*)[ |\t]*\$(?P<variable>[\w|-|_]+)[ |\t]*=[ |\t]*([\'|"](?P<value_str>(?!\")(?!\').*)?[\'|"]|(?P<value_dec>\d+|\d*\.\d+|\d+\.\d*))[ |\t]*\*/'
    
    def __init__(self, doc_string):
        self._doc_string = String_Enhanced(doc_string)
        self._variables  = dict()
        self._width      = 0
        
        matches = re.finditer(Doc_String.var_pat, self._doc_string)
        com_start_matches = re.finditer(Doc_String.com_pat, self._doc_string)

        for match, com_start_match in zip(matches, com_start_matches):
            self._variables[match.group('variable')] = Variable( match.group('variable'),
                                                                 Var_Adapter.adapt_to_str( match.group('value_str'), 
                                                                                           match.group('value_dec') ),
                                                                 Position( match.span()[0],
                                                                           match.span()[1] ),
                                                                 match.span()[0] - com_start_match.span()[0],
                                                                 Position( com_start_match.span()[0] - 2,
                                                                           com_start_match.span()[1] ) )

    def get_variables(self):
        return self._variables
    
    def count_width(self):
        widths  = List_Enhanced()
        span    = 0
        matches = re.finditer(Doc_String.width_pat, self._doc_string)

        for match in matches:
            span = match.span()
            widths.append(span[1]-span[0])
        
        self._width = widths.most_present_value()

    def update_variable(self, variable, text):
        self._variables[variable].set_text(text)

    def place_values(self):
        for var_name, var in reversed(self._variables.items()):
            self.place_value(var_name)

    def place_value(self, variable):
        var = self._variables[variable]
        to_insert = ''
        for line in var.get_lines():
            to_insert += '/*' + ' '*var.get_offset() + line + ' '*( self._width - var.get_offset() - len(line) ) + '*/\r\n'
        to_insert = to_insert[0:-2]
        self._doc_string = self._doc_string.replace_by_position( var.get_line_pos().get_start(),
                                                                var.get_line_pos().get_end(),
                                                                to_insert )
        
    def get_doc_string(self):
        return self._doc_string
    
    def read_template_from_file():
        text = ''
        try:
            text = File_Manager.read_file('template'.txt)
        except FileNotFoundError as e:
            View.display(e)


class File_Manager:
    def read_file(file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError("File '{file_path}' not found!")


class View:
    def display(text):
        print( f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S.%f")}: {text}')


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