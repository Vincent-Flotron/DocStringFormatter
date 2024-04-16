class Position:
    def __init__(self, start, end):
        self._start = start
        self._end   = end

    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end