import re

inp = '<input id="" name="fname" type="text"/>'

format = r'name=\"([a-zA-Z0-9_-]+)\"'
format2 = r"name=\'([a-zA-Z0-9_-]+)\'"

format_type = r'type=\"text\"'
format_type2 = r"type=\'text\'"

m = re.search(format, inp)

if m:
    print(type(m.group(1)))