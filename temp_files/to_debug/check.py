import parse_sql
import check_from_db
import find_select_stmt
from find_with_stmt import get_with_list
import sys

db_tables, column_info = check_from_db.get_db_info(user="ceci",
                                                   password="mimic",
                                                   host="localhost",
                                                   port="5432",
                                                   database="mimic",
                                                   schema="public")


def check_select_stmt(select_stmt, file_path):
    # print(get_with_list(file_path))
    if "targetList" in select_stmt.keys():
        # target: columns
        # source: tables
        select_targets = parse_sql.get_select_targets(select_stmt)
        select_sources = parse_sql.get_select_from(select_stmt)
        for target in select_targets:
            status = False
            # if target is in one of the source's column
            for source in select_sources:
                # if source table is in database
                if source in db_tables:
                    if target in column_info[source]:
                        status = True
                        break

                # if source table is created by with_clauses
                # in some cases the source is in both db_tables and tables created by with_clause
                if source in get_with_list(file_path).keys():
                    # print(get_with_list(file_path))
                    columns = get_with_list(file_path)[source]
                    for column in columns:
                        if column == target:
                            status = True
                            break

                if source not in db_tables and source not in get_with_list(file_path).keys():
                    sys.stderr.write("[error] table \"" + source + "\" doesn't exist" + "\n")

            if not status:
                sys.stderr.write("[error] cannot find target \"" + target + "\" from sources: " + str(select_sources) + "\n")
                # print(select_stmt)

    # if it's op, like union
    # check recursively
    elif "larg" in select_stmt.keys() and "rarg" in select_stmt.keys():
        check_select_stmt(select_stmt["larg"], file_path)
        check_select_stmt(select_stmt["rarg"], file_path)


def check_sql(sql_file_path):
    select_stmt_list = find_select_stmt.get_select_stmts(sql_file_path)
    for select_stmt in select_stmt_list:
        check_select_stmt(select_stmt, sql_file_path)

