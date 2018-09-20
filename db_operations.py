import mysql.connector
from mysql.connector import Error


class DBOperations:
    """ Class for implementing methods for MySQL database operations """
    def __init__(self, host_ip, port_no, user_name, password):
        self.host = host_ip
        self.port = port_no
        self.name = user_name
        self.pwd = password

    def connect(self, database):
        """ Connect to MySQL database """
        try:
            conn = mysql.connector.connect(host=self.host, port=self.port,
                                           user=self.name, password=self.pwd,
                                           database=database)
            if conn.is_connected():
                print("Connected to MySQL database")
                return conn
        except Error as e:
            print("Error while connecting to MySQL database : ", e)
            return False

    @staticmethod
    def execute(conn_obj, sql_select_query):
        """ Execute SQL query """
        print("Executing SQL query : ", sql_select_query)
        cursor = conn_obj.cursor()
        res = []
        try:
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            print("Total matching records found : ", records)
            res = records
        except Exception as e:
            print("Error while executing SQL query : ", e)
        finally:
            cursor.close()
            return res

    @staticmethod
    def close_connection(conn_obj):
        """ Close MySQL database connection """
        try:
            if conn_obj.is_connected():
                conn_obj.close()
                print("Connection to MySQL database is closed")
                return True
        except Exception as e:
            print("Error while closing the MySQL database connection : ", e)
            return False
