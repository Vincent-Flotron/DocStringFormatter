import os
import platform
import subprocess

class File_Manager:
    def read_file(file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError("File '{file_path}' not found!")

    def open_file_with_text_editor(path, default_editor = None):
        if not default_editor:
            default_editor = File_Manager.get_default_text_editor()
        if default_editor:
            subprocess.run([default_editor, path])
            return True
        else:
            return False

    def get_default_text_editor():
        # Determine the platform
        current_platform = platform.system()

        if current_platform == 'Linux':
            # Check if the EDITOR environment variable is set
            editor = os.getenv('EDITOR')
            if editor:
                return editor

            # If EDITOR is not set, check VISUAL environment variable
            visual = os.getenv('VISUAL')
            if visual:
                return visual

            # If neither EDITOR nor VISUAL is set, return a default value
            return 'vi'  # Default to 'vi' editor if both environment variables are not set

        elif current_platform == 'Windows':
            # Use the Windows registry to get the default text editor
            import winreg

            # Path to the registry key containing file associations for the current user
            key_path = r'Software\Classes\.txt'

            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                    value, _ = winreg.QueryValueEx(key, None)
                    return value
            except FileNotFoundError:
                return 'notepad.exe'  # Fallback to notepad.exe if the registry key is not found

        else:
            # Unsupported platform
            return None