import sqlite3

"""This class initiates a connection to the sqlite database
and returns a cursor object upon quering
"""


class DatabaseManager(object):

    """Connects to database and returns a cursor object
    """

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.commit()
        self.cur = self.conn.cursor()
        if self.gettablecount() < 2:
            self.createtables()

    """Performs a query to the database based on the supplied
    query string.This method then returns the cursor object to the
    calling class/method
    """

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    """Called when the class object is destroyed.
    """

    def __del__(self):
        # Closes the connection to the database to prevent database locks
        self.conn.close()

    """Returns list of predefined rooms
    """

    def getrooms(self):
        listoffices = [['Valhalla', 6, 'OFFICE'],
                       ['Turqois', 4, 'OFFICE'],
                       ['Oculus', 5, 'OFFICE'],
                       ['Hogwarts', 6, 'OFFICE'],
                       ['Camelot', 4, 'OFFICE'],
                       ['Midgar', 2, 'OFFICE'],
                       ['Mordor', 3, 'OFFICE'],
                       ['Narnia', 5, 'OFFICE'],
                       ['Shire', 3, 'OFFICE'],
                       ['Quiet-Room', 4, 'OFFICE']]

        listlivingspaces = [['Blue', 4, 'LIVING'],
                            ['Red', 3, 'LIVING'],
                            ['Amber', 2, 'LIVING'],
                            ['Yellow', 4, 'LIVING'],
                            ['Brown', 3, 'LIVING'],
                            ['Green', 4, 'LIVING'],
                            ['Pink', 4, 'LIVING'],
                            ['Purple', 3, 'LIVING'],
                            ['Violet', 2, 'LIVING'],
                            ['White', 4, 'LIVING']]

        rooms = listoffices + listlivingspaces
        return rooms

    """Creates database tables if they does not exist
    """

    def gettablecount(self):
        cursor = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name")
        # .fetchall returns a tuple of tuples of tablenames which we convert to a list
        tables = map(lambda t: t[0], cursor.fetchall())
        return len(tables)

    def createtables(self):
        self.query(
            "CREATE Table if not exists Allocations (_id INTEGER PRIMARY KEY AUTOINCREMENT, Personnel_Name TEXT NOT NULL, Room_type TEXT NOT NULL, Room_name TEXT NOT NULL,Personnel_type TEXT NOT NULL)")
        self.query(
            "CREATE Table if not exists Staff (_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Residing TEXT NOT NULL, Category TEXT NOT NULL)")
        self.query(
            "CREATE Table if not exists Rooms (_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Maxppl INT NOT NULL,Curppl INT NOT NULL, Room_type TEXT NOT NULL)")
        roomslist = self.getrooms()
        for entry in roomslist:
            self.query("INSERT INTO Rooms (Name, Maxppl, Curppl, Room_type)VALUES ('" +
                       entry[0] + "', '" + str(entry[1]) + "','0','" + entry[2] + "')")
