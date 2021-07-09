from fuzzers.Fuzzer import Fuzzer
import requests


class XSS(Fuzzer):

    def __init__(self, inputs, method, url):
        super(XSS, self).__init__(inputs, method, url)
    
    def attack(self):
        for key in self.inputs:
            with open('./fuzzers/xsspayloads.txt', 'r') as payloads:
                payload = payloads.readline().strip()

                # data = Dict[str, str]
                data = self.inputs.copy()

                if self.submit_name:
                    data[self.submit_name] = self.submit_value

                while payload != '':
                    data[key] = payload

                    if self.method == "get":
                        result = requests.get(self.url, data)
                    else:
                        result = requests.post(self.url, data)
                        
                    content = result.text
                    if payload in content:
                        print(f"[+] Potential xss vulneribility, payload: {payload}, url: {self.url}")
                        break
                    payload = payloads.readline()