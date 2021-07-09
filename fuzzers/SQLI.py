from fuzzers.Fuzzer import Fuzzer
from utils import colored
import requests


class SQLI(Fuzzer):

    def __init__(self, inputs, method, url, cookies):
        super(SQLI, self).__init__(inputs, method, url, cookies)

    def attack(self):
        errors = []
        with open('./fuzzers/sqlierrors.txt', 'r') as errs:
            err = errs.readline().strip()
            while(err != ''):
                errors.append(err)
                err = errs.readline().strip()

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

                if self.method.lower() == "get":
                    result = requests.get(self.url, data, cookies=self.cookies)
                else:
                    result = requests.post(
                        self.url, data, cookies=self.cookies)

                content = result.text
                for err in errors:
                    if err in content:
                        print(colored(
                            0, 255, 0, f"\t[+] Potential sql injection vulneribility, payload: {payload}, url: {self.url}"))
                        return

            payloads = ["a' or SLEEP(3); #"]
            for payload in payloads:
                data[key] = payload

                if self.method.lower() == "get":
                    result = requests.get(self.url, data, cookies=self.cookies)
                else:
                    result = requests.post(
                        self.url, data, cookies=self.cookies)

                duration = result.elapsed.total_seconds()
                if duration >= 3:
                    print(colored(
                        0, 255, 0, f"\t[+] Potential sql injection vulneribility, payload: {payload}, url: {self.url}"))
                    return
