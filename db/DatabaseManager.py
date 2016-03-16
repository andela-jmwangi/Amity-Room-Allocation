import sqlite3


class DatabaseManager(object):
    """This class initiates a connection to the sqlite database
    and returns a cursor object upon quering"""

    def __init__(self, db):
        """Connects to database and returns a cursor object"""

        self.conn = sqlite3.connect(db)  # connects to Amity.sqlite database
        self.cur = self.conn.cursor()
        # checks if atleast 1 table exists (sqlite_sequence)
        if self.get_table_count() < 2:
            self.create_tables()  # if so, create the remaining 3

    def query(self, arg):
        """Performs a query to the database based on the supplied
        query string and returns the cursor object"""

        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def __del__(self):
        """Called when the class object is destroyed."""

        # Closes the connection to the database to prevent database locks
        self.conn.close()

    def get_rooms(self):
        """Returns list of predefined rooms"""

        offices = {'Valhalla': 6, 'Turqois': 4, 'Oculus': 5, 'Hogwarts': 6, 'Camelot':
                   4, 'Midgar': 2, 'Mordor': 3, 'Narnia': 5, 'Shire': 3, 'Quiet-Room': 4}

        living_spaces = {'Blue': 4, 'Red': 3, 'Amber': 2, 'Yellow': 4, 'Brown':
                         3, 'Green': 4, 'Pink': 4, 'Purple': 3, 'Violet': 2, 'White': 4}

        all_rooms = {'OFFICE': offices, 'LIVING': living_spaces}
        return all_rooms

    def get_table_count(self):
        """Gets a the number of tables present in the database"""

        cursor = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name")
        return len(cursor.fetchall())

    def create_tables(self):
        """Creates database tables if they does not exist and populates Rooms table"""

        self.query(
            "CREATE Table if not exists Allocations (_id INTEGER PRIMARY KEY AUTOINCREMENT, Personnel_Name TEXT NOT NULL, Room_type TEXT NOT NULL, Room_name TEXT NOT NULL,Personnel_type TEXT NOT NULL)")
        self.query(
            "CREATE Table if not exists Staff (_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Residing TEXT NOT NULL, Category TEXT NOT NULL)")
        self.query(
            "CREATE Table if not exists Rooms (_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Maxppl INT NOT NULL,Curppl INT NOT NULL, Room_type TEXT NOT NULL)")
        rooms_list = self.get_rooms()  # get all rooms
        for room_type, data in rooms_list.iteritems():
            for name, num in data.iteritems():
                self.query("INSERT INTO Rooms (Name, Maxppl, Curppl, Room_type)VALUES ('" +
                           name + "', '" + str(num) + "','0','" + room_type + "')")
