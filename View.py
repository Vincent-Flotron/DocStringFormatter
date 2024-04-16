from datetime import datetime

class View:
    def display(text):
        print( f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S.%f")}: {text}')