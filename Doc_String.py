from Enhanced_Types import List_Enhanced, String_Enhanced
import re
from Variable import Variable, Var_Adapter
from Position import Position
from File_Manager import File_Manager


class Doc_String:

    def __init__(self, view):
        self._view = view
        self._text        = self.read_template_from_file()
        self._doc_string  = String_Enhanced(self._text)
        self._variables   = dict()
        self._width       = 0
        
        self._var_pat   = r'\$(?P<variable>[\w|-|_]+)[ |\t]*=[ |\t]*([\'|"](?P<value_str>(?!\")(?!\').*)?[\'|"]|(?P<value_dec>\d+|\d*\.\d+|\d+\.\d*))'
        self._width_pat = r'(?<=/\*).*(?=\*/)'
        self._com_pat   = r'(?<=/\*)[ |\t]*\$(?P<variable>[\w|-|_]+)[ |\t]*=[ |\t]*([\'|"](?P<value_str>(?!\")(?!\').*)?[\'|"]|(?P<value_dec>\d+|\d*\.\d+|\d+\.\d*))[ |\t]*\*/'
        self._param_pat = re.compile(r"(input|input-output|output|)\s*([\w|-]+)\s+as\s+([\w|-]+)")
        
        self.extract_variables()


    def extract_variables(self):
        matches           = re.finditer(self._var_pat, self._doc_string)
        com_start_matches = re.finditer(self._com_pat, self._doc_string)

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
        matches = re.finditer(self._width_pat, self._doc_string)

        for match in matches:
            span = match.span()
            widths.append(span[1]-span[0])
        
        self._width = widths.most_present_value()

    def update_variable(self, variable, text):
        self._variables[variable].set_text(text)

    def place_values_into_docstring(self):
        for var_name, var in reversed(self._variables.items()):
            self.place_value(var_name)

    def place_value(self, variable):
        var       = self._variables[variable]
        to_insert = ''
        for line in var.get_lines():
            to_insert += '/*' + ' '*var.get_offset() + line + ' '*( self._width - var.get_offset() - len(line) ) + '*/\r\n'
        to_insert        = to_insert[0:-2]
        self._doc_string = self._doc_string.replace_by_position( var.get_line_pos().get_start(),
                                                                 var.get_line_pos().get_end(),
                                                                 to_insert )
        
    def get_doc_string(self):
        return self._doc_string
    
    def read_template_from_file(self):
        text = ''
        try:
            text = File_Manager.read_file('template.txt')
        except FileNotFoundError as e:
            self._view.display(e)
        return text
    
    def extract_parameters(self, method_declaration):
        matches = self._param_pat.findall(method_declaration)
        parameters = []
        parameters = ""
        for io, param, par_type in matches:
            io = io.strip()
            param = param.strip()
            par_type = par_type.strip()
            return_txt = "returns" if io == "output" else ""
            parameters.append((param, return_txt, par_type))
        return parameters