
from DatabaseManager import DatabaseManager
from Personnel import Personnel
import random
import ipdb
import ast
from Fileparser import Fileparser
import os.path
"""This class handles all allocation tasks
"""


class Allocations(object):
    def __init__(self, importedallocations):
        # initialised list to hold persons who are qualified to be allocated
        # rooms
        self.db = DatabaseManager("Amity.sqlite")
        self.importedallocations = importedallocations
        self.qualifiedcandidates = []
        self.personelallocation = Personnel()
    """determines if personnel has a room
    """

    def runallocations(self, personnel_name, personnel_type, residing):
        # ipdb.set_trace(context=1)
        allocations_list = []
        if residing == "Y":
                # allocate both office and living space
            if self.hasroom(personnel_name, "OFFICE"):
                # no need to allocate office, try allocate living space
                allocatedroom = self.personelallocation.getroomallocated(
                    "OFFICE", personnel_name)
                print (
                    personnel_name + " has already been allocated " + allocatedroom)
                if self.hasroom(personnel_name, "LIVING"):
                    # no need to allocate living.
                    allocatedroom = self.personelallocation.getroomallocated(
                        "LIVING", personnel_name)
                    print (
                        personnel_name + " has already been allocated " + allocatedroom)
                else:
                    # doesn't have living space thus add to allocate
                    if self.areroomavailable("OFFICE"):
                        # There is an living space available, proceed to
                        # add to list of qualifiedpersonsliving

                        room_name = self.getrandomroom("OFFICE")
                        if len(room_name) > 0:
                            allocations_list.append(
                                (room_name, personnel_name))
                            self.saveallocation(
                                personnel_name, room_name, "OFFICE", personnel_type)

                    else:
                        # There is no living space available, thus inform
                        # user.
                        print (personnel_name +
                               "  =>  Sorry all living spaces have already been taken")
            else:
                # allocate only office
                if self.hasroom(personnel_name, "OFFICE"):
                    # person already has a room so no need to allocate
                    allocatedroom = self.personelallocation.getroomallocated(
                        "OFFICE", personnel_name)
                    print (
                        personnel_name + " has already been allocated " + allocatedroom)
                else:
                    # person doesn't have a room thus proceed to allocate
                    if self.areroomavailable("OFFICE"):
                    # There is an office spot available, proceed to
                    # add to list of qualifiedpersonsoffice
                        room_name = self.getrandomroom("OFFICE")
                        if len(room_name) > 0:
                            allocations_list.append(
                                (room_name, personnel_name))
                            self.saveallocation(
                                personnel_name, room_name, "OFFICE", personnel_type)
                    else:
                        # There is no office spot available, thus inform user.
                        print (personnel_name +
                               "Sorry all office spots have already been taken")
                if self.hasroom(personnel_name, "LIVING"):
                    # no need to allocate living.
                    allocatedroom = self.personelallocation.getroomallocated(
                        "LIVING", personnel_name)
                    print (
                        personnel_name + " has already been allocated " + allocatedroom)
                else:
                    # doesn't have living space thus add to allocate
                    if self.areroomavailable("LIVING"):
                        # There is an living space available, proceed to
                        # add to list of qualifiedpersonsliving
                        room_name = self.getrandomroom("LIVING")
                        if len(room_name) > 0:
                            allocations_list.append(
                                (room_name, personnel_name))
                            self.saveallocation(
                                personnel_name, room_name, "LIVING", personnel_type)
                    else:
                        # There is no living space available, thus inform
                        # user.
                        print (personnel_name +
                               "Sorry all living spaces have already been taken")
        else:
            # allocate only office
            if self.hasroom(personnel_name, "OFFICE"):
                # person already has a room so no need to allocate
                allocatedroom = self.personelallocation.getroomallocated(
                    "OFFICE", personnel_name)
                print (
                    personnel_name + " has already been allocated " + allocatedroom)
            else:
                # person doesn't have a room thus proceed to allocate
                if self.areroomavailable("OFFICE"):
                # There is an office spot available, proceed to
                # add to list of qualifiedpersonsoffice
                    room_name = self.getrandomroom("OFFICE")
                    if len(room_name) > 0:
                        allocations_list.append(
                            (room_name, personnel_name))
                        self.saveallocation(
                            personnel_name, room_name, "OFFICE", personnel_type)
                else:
                    # There is no office spot available, thus inform user.
                    print (personnel_name +
                           "Sorry all office spots have already been taken")

        return allocations_list

    def hasroom(self, personnel_name, room_type):
        # query db to check if name exists in Allocations table
        cursor = self.db.query("SELECT * from Allocations where Personnel_Name = '" +
                               personnel_name.replace("'", "") + "' and Room_type = '" + room_type + "'")
        if len(cursor.fetchall()) > 0:
            return True  # return true if one or more records have been found
        return False  # return false if no record found

    """checks whether there is a room available for a certain category i.e either office or livingspace
    """

    def areroomavailable(self, room_type):
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Maxppl > Curppl and Room_type = '" + room_type + "'")
        if len(cursor.fetchall()) > 0:
            return True  # return true if one or more records have been found
        return False  # return false if no record found

    """checks for available rooms (rooms with available slots) and returns them
    """

    def getavailablerooms(self, room_type):
        listrooms = []  # initiate empty list
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Maxppl > Curppl and Room_type = '" + room_type + "'")
        for row in cursor:
            listrooms.append(row[1])  # populate list with room names(row[1]).
        return listrooms

    def getalloccupiedrooms(self):
        listrooms = []  # initiate empty list
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Curppl > 0")
        for row in cursor:
            listrooms.append(row[1])  # populate list with room names(row[1]).
        return listrooms

    """returns a randomised list of personnel or rooms
    """

    def randomizelist(self, all):
        listrandomindices = random.sample(
            range(0, len(all)), len(all))  # generate a list with random indices.
        randomisedlist = []
        for num in listrandomindices:
            # populate randomizedlist with random entries based on
            # listrandomindices list
            randomisedlist.append(all[num])
        return randomisedlist

    """returns a dictionary of allocations
    """

    def getrandomroom(self, room_type):
        availablerooms = []
        availablerooms = self.getavailablerooms(room_type)
        random.shuffle(availablerooms)
        # ipdb.set_trace(context=1)
        return str(availablerooms[0])

    def saveallocation(self, personnel_name, room_name, room_type, personnel_type):
        self.db.query("INSERT INTO Allocations (Personnel_Name, Room_name, Personnel_type, Room_type)VALUES ('" +
                      personnel_name + "', '" + room_name + "','" + personnel_type + "','" + room_type + "')")
        self.db.query(
            "UPDATE Rooms set Curppl = Curppl + 1 where Name = '" + room_name + "'")

    def allocate(self):
        randomizedallocations = self.randomizelist(self.importedallocations)
        for element in randomizedallocations:
            personnel_name = element[0].replace("'", "")
            personnel_type = element[1]
            if len(element) == 3:
                residing = element[2]
            else:
                residing = 'N'
            self.qualifiedcandidates.append(self.runallocations(
                personnel_name, personnel_type, residing))

        list2 = [x for x in self.qualifiedcandidates if x != []]
        if list2:
            with open("cache", "w") as text_file:
                text_file.write(str(list2))
            print list2

    def unallocated(self):
        original_list_names = []
        allocated_list_names = []
        for item in self.get_list_imported_names():
            original_list_names.append(item[0])

        for item in self.readcache():
            for itemtuple in item:
                allocated_list_names.append(itemtuple[1])

        list_unallocated = self.personelallocation.getunallocated(
            allocated_list_names, original_list_names)
        return list_unallocated

    def get_list_imported_names(self):
        if os.path.exists('filepath'):
            with open('filepath') as f:
                contents = f.read()
                parser = Fileparser(contents)
                inputlist = parser.getlinecontents()
                return inputlist
        else:
            print "The file does not exist"

    def readcache(self):
        with open('cache') as f:
            contents = f.read()
            return ast.literal_eval(contents)
