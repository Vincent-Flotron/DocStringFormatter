import configparser
import os

class Config:

    def __init__( self, controller ):
        self._config_file_path = "config.ini"
        self._config           = self._read_config_file()
        self._controller       = controller


    def _read_config_file( self ):
        config = configparser.ConfigParser()
        config.read(self._config_file_path)
        return config
    
    def get_setting(self, section, setting):
        if section in self._config and setting in self._config[section]:
            return self._config[section][setting]
        else:
            return None
        
    def _set_setting(self, section, setting, value):
        if section not in self._config:
            self._config[section] = {}
        self._config[section][setting] = value
        with open(self._config_file_path, 'w') as configfile:
            self._config.write(configfile)

    
    def edit_setting(self, section, setting, new_value):
        previous_value = self.get_setting(section, setting)
        # Update the config file with the new value
        self._set_setting(section, setting, new_value)
        return f"Setting '{setting}' in section '{section}' updated successfully from '{previous_value}' to '{new_value}'."


    def get_default_editor(self):
        return self.get_setting('DEFAULT', 'text_editor')

    # def edit_default_editor(self, default_editor):
    #     return self.edit_setting('DEFAULT', 'text_editor', default_editor)

    def edit_default_editor( self ):
        self._controller.edit_setting( 'DEFAULT', 'text_editor' )
    
    def get_comment_start( self ):
        return self.get_setting('COMMENT', 'comment_start')
    
    def edit_comment_start(self):
        self._controller.edit_setting('COMMENT', 'comment_start')

    def get_comment_end( self ):
        return self.get_setting('COMMENT', 'comment_end')
    
    def edit_comment_end(self):
        self._controller.edit_setting('COMMENT', 'comment_end')

    def get_nb_indent( self ):
        return self.get_setting('CODE', 'code_indent')

    def edit_nb_indentation(self):
        self.edit_setting('CODE', 'code_indent')