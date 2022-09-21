
def parse_join_expr(join_stmt, relname_list):
    if "larg" in join_stmt:
        if "JoinExpr" in join_stmt["larg"].keys():
            relname_list = parse_join_expr(join_stmt["larg"]["JoinExpr"], relname_list)
        if "RangeVar" in join_stmt["larg"].keys():
            # for source table, choose relname instead of alias
            relname_list.append(join_stmt["larg"]["RangeVar"]["relname"])

    if "rarg" in join_stmt:
        if "JoinExpr" in join_stmt["rarg"].keys():
            relname_list = parse_join_expr(join_stmt["rarg"]["JoinExpr"], relname_list)
        if "RangeVar" in join_stmt["rarg"].keys():
            relname_list.append(join_stmt["rarg"]["RangeVar"]["relname"])

    return relname_list


def get_select_from(select_stmt):
    from_clauses = select_stmt["fromClause"]
    relnames = []
    for from_clause in from_clauses:
        # if is not join_expr:
        if "RangeVar" in from_clause.keys():
            relnames.append(from_clause["RangeVar"]["relname"])

        # if is join_expr, parse it recursively
        elif "JoinExpr" in from_clause.keys():
            relnames = parse_join_expr(from_clause["JoinExpr"], relnames)

        # if is subselect
        elif "RangeSubselect" in from_clause.keys():
            res = get_select_from(from_clause["RangeSubselect"]["subquery"]["SelectStmt"])
            for name in res:
                relnames.append(name)

    return relnames


def get_select_targets(select_stmt):
    target_list = select_stmt["targetList"]
    targets = []
    for target in target_list:
        target_val = target["ResTarget"]["val"]
        if "ColumnRef" in target_val.keys():
            # another key may be 'A_Star'
            if "String" in target_val["ColumnRef"]["fields"][-1]:
                targets.append(target_val["ColumnRef"]["fields"][-1]["String"]["str"])
        if "FuncCall" in target_val:
            # some func call doesn't have "args"
            if "args" in target_val["FuncCall"].keys():
                target_args = target_val["FuncCall"]["args"]
                for arg in target_args:
                    if "ColumnRef" in arg.keys():
                        targets.append(arg["ColumnRef"]["fields"][-1]["String"]["str"])

    return targets



