import os
from check import check_sql


def main():
    sql_path = "sql_files"
    sql_file_list = os.listdir(sql_path)
    for sql_file in sql_file_list:
        print("\nchecking file: " + sql_file + "...")
        full_path = os.path.join(sql_path, sql_file)
        check_sql(full_path)


if __name__ == "__main__":
    main()
