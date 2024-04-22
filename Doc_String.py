from Enhanced_Types import List_Enhanced, String_Enhanced
import re
from Section import Section, Adapter, Parameter
from Position import Position
from File_Manager import File_Manager


class Doc_String:

    def __init__(self, view, config):
        self._config        = config
        self._view          = view
        template_from_file  = self._read_template_from_file()
        self._doc_string    = String_Enhanced(template_from_file)
        self._template      = String_Enhanced(template_from_file)
        self._sections      = dict()
        self._width         = 0
        self._comment_start = config.get_comment_start()   or '/*'
        self._comment_end   = config.get_comment_end()     or '*/'
        self._nb_indent     = int(config.get_nb_indent())  or 2
        
        self._var_pat   = r'\$(?P<section>[\w|-|_]+)[ |\t]*=[ |\t]*([\'|"](?P<value_str>(?!\")(?!\').*)?[\'|"]|(?P<value_dec>\d+|\d*\.\d+|\d+\.\d*))'
        self._width_pat = r'(?<=/\*).*(?=\*/)'
        self._com_pat   = r'(?<=/\*)[ |\t]*\$(?P<section>[\w|-|_]+)[ |\t]*=[ |\t]*([\'|"](?P<value_str>(?!\")(?!\').*)?[\'|"]|(?P<value_dec>\d+|\d*\.\d+|\d+\.\d*))[ |\t]*\*/'
        self._param_pat = re.compile(r"(input|input-output|output|)\s*([\w|-]+)\s+as\s+([\w|-]+)")
        
        self._previous_parameters = {}
        self._parameter_section   = 'Parameters'
        
        self._extract_sections_from_template()

        self.count_width()


    def _extract_sections_from_template(self):
        matches           = re.finditer(self._var_pat, self._template)
        com_start_matches = re.finditer(self._com_pat, self._template)

        for match, com_start_match in zip(matches, com_start_matches):
            self._sections[match.group('section')] = Section( match.group('section'),
                                                                 Adapter.adapt_to_str( match.group('value_str'), 
                                                                                           match.group('value_dec') ),
                                                                 Position( match.span()[0],
                                                                           match.span()[1] ),
                                                                 match.span()[0] - com_start_match.span()[0],
                                                                 Position( com_start_match.span()[0] - 2,
                                                                           com_start_match.span()[1] ) )


    def add_parameter( self, parameter ):
        section_name = self._parameter_section
        if self._sections[section_name] is not None:
            self._sections[section_name].add_parameter(parameter)
        else:
            raise Exception( f'section {section_name} doesn\'t exist!' )
        
    def update_parameter( self, name, new_text):
        params = self.get_parameters_section().get_parameters()
        self.get_parameters_section().get_parameters()[name].set_text(new_text)

    def get_sections( self ):
        return self._sections
    
    def count_width( self ):
        widths  = List_Enhanced()
        span    = 0
        matches = re.finditer(self._width_pat, self._template)

        for match in matches:
            span = match.span()
            widths.append(span[1]-span[0])
        
        self._width = widths.most_present_value()

    def update_section( self, section, text ):
        self._sections[section].set_text(text)
        
    def generate_doc_string( self ):
        self._doc_string = self._template
        for name, section in reversed(self._sections.items()):
            self.place_value(name)

    def place_value( self, section_name ):
        section   = self._sections[section_name]

        # INSERT PARAMETERES HERE
        if section.has_parameters():
            self._view.display('# INSERT PARAMETERES HERE')

        to_insert = ''
        for line in section.get_lines():
            to_insert += self._comment_start + ' '*section.get_offset() + line + ' '*( self._width - section.get_offset() - len(line) ) + self._comment_end + '\r\n'
        to_insert        = to_insert[0:-2]
        self._doc_string = self._doc_string.replace_by_position( section.get_line_pos().get_start(),
                                                                 section.get_line_pos().get_end(),
                                                                 to_insert )
        
    def get_doc_string( self ):
        return self._doc_string
    
    def _read_template_from_file(self):
        text = ''
        try:
            text = File_Manager.read_file( 'template.txt' )
        except FileNotFoundError as e:
            self._view.display(e)
        return text
    
    def extract_parameters_from_method( self, method_declaration ):
        matches = self._param_pat.findall( method_declaration )
        parameters = {}
        for io, param, par_type in matches:
            io = io.strip()
            param = param.strip()
            par_type = par_type.strip()
            return_txt = "returns" if io == "output" else ""
            parameters[param] = Parameter( param, f'{Adapter.add_sep_after(return_txt)}{par_type}' )

        self.update_parameters(parameters)


    def update_parameters(self, parameters):
        new_parameter         = ''
        new_parameter_cpt     = 0
        lost_parameter        = ''
        lost_parameter_cpt    = 0
        for _, param in parameters.items():
            if not param.get_name() in self._previous_parameters:
                new_parameter += param.get_name()
                new_parameter_cpt += 1
            
        for key, previous_parameter in self._previous_parameters.items():
            if not previous_parameter.get_name() in parameters:
                lost_parameter += previous_parameter.get_name()
                lost_parameter_cpt += 1

        if lost_parameter_cpt == 1 and new_parameter_cpt == 1:
            self._rename_parameter(lost_parameter, new_parameter)

        if lost_parameter_cpt > 1:
            self._delete_all_parameters()

        self._add_only_new_parameters(parameters)
        self._previous_parameters = self.get_parameters_section().get_parameters()

    def _delete_all_parameters(self):
        self.get_parameters_section().remove_all_parameters()

    def get_parameters_section( self ):
        return self._sections[self._parameter_section]

    def _rename_parameter(self, target, new_name):
        parameter_to_rename = self._previous_parameters[target]
        copy_of_parameter = parameter_to_rename.deep_copy()
        copy_of_parameter.set_name(new_name)
        del self._previous_parameters[target]
        self._previous_parameters[new_name] = copy_of_parameter

    def _add_only_new_parameters(self, parameters):
        for key, param in parameters.items():
            if param.get_name() not in self._previous_parameters:
                self.get_parameters_section().add_parameter( param.deep_copy() )  
