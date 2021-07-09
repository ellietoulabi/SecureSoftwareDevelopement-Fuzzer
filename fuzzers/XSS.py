from fuzzers.Fuzzer import Fuzzer
import requests
from utils import colored


class XSS(Fuzzer):

    def __init__(self, inputs, method, url, cookies):
        super(XSS, self).__init__(inputs, method, url, cookies)

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

                    if self.method.lower() == "get":
                        result = requests.get(
                            self.url, data, cookies=self.cookies)
                    else:
                        result = requests.post(
                            self.url, data, cookies=self.cookies)

                    content = result.text
                    if payload in content:
                        print(colored(
                            0, 255, 0, f"\t[+] Potential xss vulneribility, payload: {payload}, url: {self.url}"))
                        break
                    payload = payloads.readline().strip()
