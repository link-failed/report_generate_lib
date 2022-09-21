import re
import json
import pglast


def process_sql(file_path):
    with open(file_path, 'r') as sql_file:
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
    return s

    # no need to write back
    # with open('test.sql', 'w') as sql_file:
    #     sql_file.write(s)


def is_json(value):
    if str(value)[0] == '{' and str(value)[-1] == '}':
        return True
    else:
        return False


def find_select_stmts(query_json, select_stmt_list):
    if is_json(query_json):
        for key, value in query_json.items():
            if key == "SelectStmt":
                select_stmt_list.append(query_json["SelectStmt"])
                # if there is with clause in this stmt
                if "withClause" in value:
                    select_stmt_list = find_select_stmts(value, select_stmt_list)

            elif is_json(str(value)):
                select_stmt_list = find_select_stmts(value, select_stmt_list)

            elif str(value)[0] == '[' and str(value)[-1] == ']':
                for i in value:
                    select_stmt_list = find_select_stmts(i, select_stmt_list)
    return select_stmt_list


def get_select_stmts(sql_file_path):
    select_stmt_list = []
    query_str = process_sql(sql_file_path)
    query_json = json.loads(pglast.parser.parse_sql_json(query_str))
    find_select_stmts(query_json, select_stmt_list)
    return select_stmt_list
