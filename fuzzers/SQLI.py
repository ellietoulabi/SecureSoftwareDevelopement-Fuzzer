from fuzzers.Fuzzer import Fuzzer
import requests


class SQLI(Fuzzer):

    def __init__(self, inputs, method, url):
        super(SQLI, self).__init__(inputs, method, url)
    
    def attack(self):
        errors = []
        with open('./fuzzers/sqlierrors.txt', 'r') as errs:
            err = errors.append(errs.readline().strip())
        
        
        for key in self.inputs:

            data = self.inputs.copy()

            for i in data:
                if i != key:
                    if data[i] == '':
                        data[i] = 'a'
            
            if self.submit_name:
                data[self.submit_name] = self.submit_value

            payloads = ['"', "'"]
            for payload in payloads:
                data[key] = payload

                if self.method == "get":
                    result = requests.get(self.url, data)
                else:
                    result = requests.post(self.url, data)
                
                content = result.text
                for err in errors:
                    if err in content:
                        print(f"[+] Potential sql injection vulneribility, payload: {payload}, url: {self.url}")
                        return