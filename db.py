items = {}
import sqlite3

class DataBase:
    connection_string = "stores_db.db"

    @classmethod
    def initialize_db(cls,con_str = None):
        if con_str is not None:
            cls.connection_string = con_str
        with sqlite3.connect(cls.connection_string) as con:
            cur = con.cursor()
            try:
                cur.execute("""CREATE TABLE IF NOT EXISTS STORES (STORE_ID INTEGER, STORE_NAME VARCHAR NOT NULL, PRIMARY KEY (STORE_ID))""")
                cur.execute("""CREATE TABLE IF NOT EXISTS ITEMS (ITEM_ID INTEGER, ITEM_NAME VARCHAR NOT NULL, ITEM_PRICE DECIMAL, STORE_ID INTEGER, PRIMARY KEY (ITEM_ID), FOREIGN KEY (STORE_ID) REFERENCES STORES(STORE_ID));""")
            except sqlite3.OperationalError as e:
                con.rollback()
                print("Error while creating database schema table")
                raise Exception("Error while creating database schema table")

    @classmethod
    def execute_query(cls,query):
        with sqlite3.connect(cls.connection_string) as connection:
            cursor = connection.cursor()
            result = cursor.execute(query)
            # try:
            # except sqlite3.Error as e:
            #     print(e)
            #     raise Exception("Incorrect query")
            # headers = [column[0] for column in cursor.description]
            return result.fetchall()
# print(DataBase.execute_query("SELECT * FROM STORES"))

def jsonify(header, query_output, key=None):
    if key is None:
        result_list = [dict(zip(header,row)) for row in query_output]
        return result_list
    else:
        result_dict = {}
        for row in query_output:
            row_json = dict(zip(header,row))
            result_dict[row_json[key]] = row_json
        return result_dict
