from find_select_stmt import get_select_stmts


'''
    with stmt format:
    ctename: [ResTarget1, ResTarget2, ResTarget3]
'''
def parse_with_clause(with_stmt):
    res = {}
    with_clauses = with_stmt["ctes"]
    for with_clause in with_clauses:
        targets = []
        cte_name = with_clause["CommonTableExpr"]["ctename"]
        target_list = with_clause["CommonTableExpr"]["ctequery"]["SelectStmt"]["targetList"]
        for target in target_list:
            if "name" in target["ResTarget"].keys():
                targets.append(target["ResTarget"]["name"])

            # if it's an A_Star Expr, there will not be "String"
            elif "String" in target["ResTarget"]["val"]["ColumnRef"]["fields"][-1].keys():
                targets.append(target["ResTarget"]["val"]["ColumnRef"]["fields"][-1]["String"]["str"])
        res[cte_name] = targets

    return res


def get_with_list(file_path):
    with_list = {}
    select_stmt_list = get_select_stmts(file_path)
    for stmt in select_stmt_list:
        if "withClause" in stmt:
            with_info = parse_with_clause(stmt["withClause"])
            with_list = dict(with_list, **with_info)
    return with_list
