class List_Enhanced(list):
    def most_present_value(self):
        vals_scores = dict()
        
        # Count occurrences of each value in the list
        for val in self:
            score            = vals_scores.get(val, 0) + 1
            vals_scores[val] = score
        
        # Find the value with the highest occurrence
        score_max = 0
        val_most_present = None
        for val, score in vals_scores.items():
            if score > score_max:
                score_max = score
                val_most_present = val

        return val_most_present
    
class String_Enhanced(str):
    def replace_by_position(self, start_pos, end_pos, replacement_string):
        repl = String_Enhanced(self[:start_pos] + replacement_string + self[end_pos:])
        return repl