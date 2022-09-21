import re

s = ""
with open('to_debug/sql_files/test.sql', 'r') as sql_file:
    sql_file = open("to_debug/sql_files/test.sql", "r")
    s = sql_file.read()
    rule1 = r'{{(.*?)}}'
    slotList = re.findall(rule1, s)
    for slot in slotList:
        rule2 = r"'(.*?)'"
        rule3 = r'"(.*?)"'
        if len(re.findall(rule2, slot)) > 0:
            new = re.findall(rule2, slot)[0]
        elif len(re.findall(rule3, slot)) > 0:
            new = re.findall(rule3, slot)[0]
        old = "{{" + slot + "}}"
        s = s.replace(old, new)

with open('to_debug/sql_files/test.sql', 'w') as sql_file:
    sql_file.write(s)

