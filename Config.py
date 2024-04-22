import configparser
import os

class Config:

    def __init__( self ):
        self._config_file_path = "config.ini"
        self._config           = self._read_config_file()


    def _read_config_file( self ):
        config = configparser.ConfigParser()
        config.read(self._config_file_path)
        return config

    def get_default_editor(self):
        if 'DEFAULT' in self._config:
            return self._config['DEFAULT'].get('text_editor', '')
        else:
            return None

    def edit_default_editor(self):
        previous_text_editor = self.get_default_editor()

        # Prompt the user to enter the default text editor
        default_editor = input(f"Enter the default text editor [{previous_text_editor}] (leave empty to keep current): ").strip()

        # Update the config file with the default text editor
        if 'DEFAULT' not in self._config:
            self._config['DEFAULT'] = {}
        self._config['DEFAULT']['text_editor'] = default_editor

        # Write the updated config file
        with open(self._config_file_path, 'w') as configfile:
            self._config.write(configfile)

        return f"Default text editor updated successfully from '{previous_text_editor}' to '{default_editor}'."