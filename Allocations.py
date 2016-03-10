
from DatabaseManager import DatabaseManager
from Personnel import Personnel
import random
import ipdb

"""This class handles all allocation tasks
"""


class Allocations(object):
    def __init__(self, importedallocations):
        # initialised list to hold persons who are qualified to be allocated
        # rooms
        self.db = DatabaseManager("Amity.sqlite")
        self.importedallocations = importedallocations

    """determines if personnel has a room
    """

    def runallocations(self, personnel_name, personnel_type, residing):
        #ipdb.set_trace(context=1)
        
        self.personelallocation = Personnel(
            personnel_name, residing, "FELLOW")
        qualifiedpersonsoffice = []
        qualifiedpersonsliving = []
        if residing == "Y":
                # allocate both office and living space
            if self.hasroom(personnel_name, "OFFICE"):
                # no need to allocate office, try allocate living space
                allocatedroom = self.personelallocation.getroomallocated(
                    "OFFICE")
                print (
                    personnel_name + " has already been allocated " + allocatedroom)
                if self.hasroom(personnel_name, "LIVING"):
                    # no need to allocate living.
                    allocatedroom = self.personelallocation.getroomallocated(
                        "LIVING")
                    print (
                        personnel_name + " has already been allocated " + allocatedroom)
                else:
                    # doesn't have living space thus add to allocate
                    if self.areroomavailable("OFFICE"):
                        # There is an living space available, proceed to
                        # add to list of qualifiedpersonsliving
                        qualifiedpersonsliving.append(personnel_name)
                    else:
                        # There is no living space available, thus inform
                        # user.
                        print (
                            "Sorry all living spaces have already been taken")
            else:
                # allocate only office
                if self.hasroom(personnel_name, "OFFICE"):
                    # person already has a room so no need to allocate
                    allocatedroom = self.personelallocation.getroomallocated(
                        "OFFICE")
                    print (
                        personnel_name + " has already been allocated " + allocatedroom)
                else:
                    # person doesn't have a room thus proceed to allocate
                    if self.areroomavailable("OFFICE"):
                    # There is an office spot available, proceed to
                    # add to list of qualifiedpersonsoffice
                        qualifiedpersonsoffice.append(personnel_name)
                    else:
                        # There is no office spot available, thus inform user.
                        print (
                            "Sorry all office spots have already been taken")
                if self.hasroom(personnel_name, "LIVING"):
                    # no need to allocate living.
                    allocatedroom = self.personelallocation.getroomallocated(
                        "LIVING")
                    print (
                        personnel_name + " has already been allocated " + allocatedroom)
                else:
                    # doesn't have living space thus add to allocate
                    if self.areroomavailable("OFFICE"):
                        # There is an living space available, proceed to
                        # add to list of qualifiedpersonsliving
                        qualifiedpersonsliving.append(personnel_name)
                    else:
                        # There is no living space available, thus inform
                        # user.
                        print (
                            "Sorry all living spaces have already been taken")
        else:
            # allocate only office
            if self.hasroom(personnel_name, "OFFICE"):
                # person already has a room so no need to allocate
                allocatedroom = self.personelallocation.getroomallocated(
                    "OFFICE")
                print (
                    personnel_name + " has already been allocated " + allocatedroom)
            else:
                # person doesn't have a room thus proceed to allocate
                if self.areroomavailable("OFFICE"):
                # There is an office spot available, proceed to
                # add to list of qualifiedpersonsoffice
                    qualifiedpersonsoffice.append(personnel_name)
                else:
                    # There is no office spot available, thus inform user.
                    print (
                        "Sorry all office spots have already been taken")

        return {"living": qualifiedpersonsliving, "office": qualifiedpersonsoffice}

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
        allrooms = self.db.getrooms()
        livingspaces = filter(lambda lvn: 'LIVING' in lvn, allrooms)
        offices = filter(lambda lvn: 'OFFICE' in lvn, allrooms)
        if room_type == "OFFICE":
            return random.shuffle(offices)
        else:
            return random.shuffle(livingspaces)

    def allocate(self):
        randomizedallocations = self.randomizelist(self.importedallocations)
        for element in randomizedallocations:
            personnel_name = element[0]
            personnel_type = element[1]
            if len(element) == 3:
                residing = element[2]
            else:
                residing = 'N'
            qualifiedcandidates = self.runallocations(
                personnel_name, personnel_type, residing)
            print qualifiedcandidates

        # allocations = {} #initiate allocations dict
        # i = 0
        # for person in listpersonnel:
        # allocations[person] = listrooms[i] # create dict with person and room allocated to.
        #     i += 1
        # return allocations
