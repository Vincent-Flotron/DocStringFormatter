class File_Manager:
    def read_file(file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError("File '{file_path}' not found!")
