import re

class Section:
    def __init__(self, name, text, position, offset, line_position):
        self._name       = name
        self._text       = text
        self._position   = position
        self._offset     = offset
        self._text       = ''
        self._line_pos   = line_position
        self._parameters = {}

    def add_parameter(self, parameter):
        if parameter.get_order() == 0:
            parameter.set_order( self.next_order())
        self._parameters[parameter.get_name()] = parameter


    def sort_parameters_by_order( self ):
        if len(self._parameters) == 0:
            return self._parameters

        # Sort the dictionary parameters by the value of the 'order' property in ascending order
        sorted_params = {}
        sorted_tuples = sorted(self._parameters.items(), key=lambda x: x[1].get_order())
        for name, parameter in sorted_tuples:
            sorted_params[name] = parameter
        return sorted_params
    
    def get_last_param_order( self ):
        pars = self.get_parameters()
        if len(pars) > 0:
            max_order = max([item.get_order() for item in self.get_parameters().values()])
        else:
            max_order = 0
        return max_order
        
    
    def next_order( self ):
        return self.get_last_param_order() + 1
    
    def remove_all_parameters(self):
        self._parameters = {}

    def get_parameters(self):
        return self._parameters

    def get_name(self):
        return self._name
    
    def set_text(self, text):
        self._text = text
    
    def get_text(self):
        return self._text
    
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


class Parameter:
    def __init__( self, name, text, order = 0 ):
        self._name  = name
        self._text  = text
        self._order = order

    def get_name( self ):
        return self._name
    
    def set_name( self, new_name ):
        self._name = new_name
    
    def set_text( self, new_text ):
        self._text = new_text
    
    def get_text( self ):
        return self._text
    
    def get_order( self ):
        return self._order
    
    def set_order( self, order ):
        self._order = order
    
    def deep_copy( self ):
        return Parameter( self.get_name(), self.get_text(), self.get_order() )
    


class Adapter:
    def adapt_to_str(string_value, decimal_value):
        if string_value != None:
            return string_value
        elif decimal_value != None:
            return str(decimal_value)
        else:
            return ''
        
    def add_sep_after(txt):
        if txt != '':
            return f'{txt} '
        else:
         return '' 