# a cursor is the object we use to interact with the database
import pymysql.cursors

# this class will give an instance of a connection to the database
class MySQLConnection:
    def __init__(self, db):
# connect
        connection = pymysql.connect(host = 'localhost', user = 'root', password = 'root', db = db, charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor, autocommit = True)
# establish the connection to the database
        self.connection = connection

# the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)

# INSERT queries will return the ID NUMBER of the row inserted
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid

# SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result

# UPDATE and DELETE queries will return nothing
                else:
                    self.connection.commit()

# if the query fails the method will return FALSE
            except Exception as e:
                print("Something went wrong", e)
                return False

# close the connection
            finally:
                self.connection.close()

# receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)