from abc import abstractclassmethod
import re

class Fuzzer:

    inputs = dict()
    method = str()
    url = str()
    submit_name = str('')
    submit_value = str('')


    def __init__(self, inputs, method, url):
        self.inputs = self.extract_inputs(inputs)
        self.method = method
        self.url = url
    

    def extract_inputs(self, inputs):
        
        result_inputs = dict()
        for inp in inputs:
            format_name = r'name=\"(.[^ ]+)\"'
            format_type = r'type=\"text\"'
            format_submit = r'type=\"submit\"'
            format_value = r'value=\"(.[^ ]+)\"'
            # TODO: Format hidden

            match_value = re.search(format_value, inp)
            val = match_value.group(1) if match_value else ""
            match_name = re.search(format_name, inp)


            if not match_name:
                continue
            
            match_type = re.search(format_type, inp)
            if not match_type:
                match_submit = re.search(format_submit, inp)
                
                if not match_submit:
                    continue
                
                self.submit_name = match_name.group(1)
                self.submit_value = val

            
            result_inputs[match_name.group(1)] = val
        
        
        return result_inputs



    @abstractclassmethod
    def attack(self): raise NotImplementedError

    