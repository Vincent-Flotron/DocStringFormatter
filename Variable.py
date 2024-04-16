import re

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