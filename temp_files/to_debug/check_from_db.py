import psycopg2


def get_table_info(user, password, host, port, database, schema):
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)

    table_list = []
    full_list = {}
    try:
        cursor = connection.cursor()
        query_str = """
            select tablename FROM pg_tables WHERE schemaname = 
        """
        query_str = query_str + "'" + schema + "';"
        cursor.execute(query_str)
        table_records = cursor.fetchall()

        for table_name in table_records:
            table_list.append(table_name[0])

        for table_name in table_list:
            # print("table_name: " + table_name)
            query_str = """
                select column_name from information_schema.columns 
                where table_schema='public' and table_name=
            """
            query_str += "'" + table_name + "'"
            cursor.execute(query_str)
            column_records = cursor.fetchall()
            column_list = []
            for record in column_records:
                column_list.append(record[0])

            full_list[table_name] = column_list

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL: ", error)
        cursor = connection.cursor()

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return table_list, full_list


def get_db_info(user, password, host, port, database, schema):
    db_tables, column_info = get_table_info(user, password, host, port, database, schema)
    return db_tables, column_info
