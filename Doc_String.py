from Enhanced_Types import List_Enhanced, String_Enhanced
import re
from Variable import Variable, Var_Adapter
from Position import Position

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
