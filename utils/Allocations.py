from db.DatabaseManager import DatabaseManager
from models.Personnel import Personnel
import random
import ipdb
import ast
from utils.FileParser import FileParser
import os.path
from colorama import Fore


class Allocations(object):
    """This class handles all allocation tasks"""

    def __init__(self, imported_allocations):
        # initialised list to hold persons who are qualified to be allocated
        # rooms
        self.db = DatabaseManager("Amity.sqlite")
        self.imported_allocations = imported_allocations
        self.qualified_candidates = []
        self.personel_allocation = Personnel()

    def run_allocations(self, personnel_name, personnel_type, residing):
        """determines if personnel has a room"""
        # ipdb.set_trace(context=1)
        allocations_list = []
        if residing == "Y":
                # allocate both office and living space
            if self.has_room(personnel_name, "OFFICE"):
                # no need to allocate office, try allocate living space
                allocated_room = self.personel_allocation.get_room_allocated(
                    "OFFICE", personnel_name)
                print ("==> " + Fore.YELLOW +
                       personnel_name + " has already been allocated " + Fore.GREEN + allocated_room + Fore.RESET)
                if self.has_room(personnel_name, "LIVING"):
                    # no need to allocate living.
                    allocated_room = self.personel_allocation.get_room_allocated(
                        "LIVING", personnel_name)
                    print ("==> " + Fore.YELLOW +
                           personnel_name + " has already been allocated " + Fore.GREEN + allocated_room + Fore.RESET)
                else:
                    # doesn't have living space thus add to allocate
                    if self.are_room_available("LIVING"):
                        # There is an living space available, proceed to
                        # add to list of qualifiedpersonsliving

                        room_name = self.get_random_room("LIVING")
                        if len(room_name) > 0:
                            allocations_list.append(
                                (room_name, personnel_name))
                            self.save_allocation(
                                personnel_name, room_name, "LIVING", personnel_type)

            else:
                # allocate only office
                if self.has_room(personnel_name, "OFFICE"):
                    # person already has a room so no need to allocate
                    allocated_room = self.personel_allocation.get_room_allocated(
                        "OFFICE", personnel_name)
                    print (
                        personnel_name + " has already been allocated " + allocated_room + Fore.RESET)
                else:
                    # person doesn't have a room thus proceed to allocate
                    if self.are_room_available("OFFICE"):
                    # There is an office spot available, proceed to
                    # add to list of qualifiedpersonsoffice
                        room_name = self.get_random_room("OFFICE")
                        if len(room_name) > 0:
                            allocations_list.append(
                                (room_name, personnel_name))
                            self.save_allocation(
                                personnel_name, room_name, "OFFICE", personnel_type)

                if self.has_room(personnel_name, "LIVING"):
                    # no need to allocate living.
                    allocated_room = self.personel_allocation.get_room_allocated(
                        "LIVING", personnel_name)
                    print ("==> " + Fore.YELLOW +
                           personnel_name + " has already been allocated " + Fore.GREEN + allocated_room + Fore.RESET)
                else:
                    # doesn't have living space thus add to allocate
                    if self.are_room_available("LIVING"):
                        # There is an living space available, proceed to
                        # add to list of qualifiedpersonsliving
                        room_name = self.get_random_room("LIVING")
                        if len(room_name) > 0:
                            allocations_list.append(
                                (room_name, personnel_name))
                            self.save_allocation(
                                personnel_name, room_name, "LIVING", personnel_type)
        else:
            # allocate only office
            if self.has_room(personnel_name, "OFFICE"):
                # person already has a room so no need to allocate
                allocated_room = self.personel_allocation.get_room_allocated(
                    "OFFICE", personnel_name)
                print ("==> " + Fore.YELLOW +
                       personnel_name + " has already been allocated " + Fore.GREEN + allocated_room + Fore.RESET)
            else:
                # person doesn't have a room thus proceed to allocate
                if self.are_room_available("OFFICE"):
                    room_name = self.get_random_room("OFFICE")
                    if len(room_name) > 0:
                        allocations_list.append(
                            (room_name, personnel_name))
                        self.save_allocation(
                            personnel_name, room_name, "OFFICE", personnel_type)

        return allocations_list

    def has_room(self, personnel_name, room_type):
        # query db to check if name exists in Allocations table
        cursor = self.db.query("SELECT * from Allocations where Personnel_Name = '" +
                               personnel_name.replace("'", "") + "' and Room_type = '" + room_type + "'")
        if len(cursor.fetchall()) > 0:
            return True  # return true if one or more records have been found
        return False  # return false if no record found

    def are_room_available(self, room_type):
        """checks whether there is a room available for a certain category i.e either office or livingspace"""
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Maxppl > Curppl and Room_type = '" + room_type + "'")
        if len(cursor.fetchall()) > 0:
            return True  # return true if one or more records have been found
        return False  # return false if no record found

    def get_available_rooms(self, room_type):
        """checks for available rooms per type (rooms with available slots) and returns them"""

        list_rooms = []  # initiate empty list
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Maxppl > Curppl and Room_type = '" + room_type + "'")
        for row in cursor:
            list_rooms.append(row[1])  # populate list with room names(row[1]).
        return list_rooms

    def get_all_occupied_rooms(self):
        """returns rooms that have atleast 1 occupant"""

        list_rooms = []  # initiate empty list
        # query db to check if a room exists with less occupants than its
        # maximum capacity
        cursor = self.db.query(
            "SELECT * from Rooms where Curppl > 0")
        for row in cursor:
            list_rooms.append(row[1])  # populate list with room names(row[1]).
        return list_rooms

    def randomize_list(self, all):
        """returns a randomised list of personnel or rooms"""
        list_random_indices = random.sample(
            range(0, len(all)), len(all))  # generate a list with random indices.
        randomised_list = []
        for num in list_random_indices:
            # populate randomizedlist with random entries based on
            # listrandomindices list
            randomised_list.append(all[num])
        return randomised_list

    def get_random_room(self, room_type):
        """returns a dictionary of allocations"""
        available_rooms = []
        available_rooms = self.get_available_rooms(room_type)
        random.shuffle(available_rooms)
        # ipdb.set_trace(context=1)
        return str(available_rooms[0])

    def save_allocation(self, personnel_name, room_name, room_type, personnel_type):
        """saves allocations to the db"""
        self.db.query("INSERT INTO Allocations (Personnel_Name, Room_name, Personnel_type, Room_type)VALUES ('" +
                      personnel_name + "', '" + room_name + "','" + personnel_type + "','" + room_type + "')")
        self.db.query(
            "UPDATE Rooms set Curppl = Curppl + 1 where Name = '" + room_name + "'")

    def allocate(self):
        """ run allocations for the input lines"""
        randomized_allocations = self.randomize_list(self.imported_allocations)
        for element in randomized_allocations:
            personnel_name = element[0].replace("'", "")
            personnel_type = element[1]
            if len(element) == 3:
                residing = element[2]
            else:
                residing = 'N'
            self.qualified_candidates.append(self.run_allocations(
                personnel_name, personnel_type, residing))

        list2 = [x for x in self.qualified_candidates if x != []]
        if len(list2) > 0:
            with open("cache", "w+") as text_file:
                text_file.write(str(list2))
        return list2

    def unallocated(self):
        """Retrieves a list of unallocated personnel"""
        original_list_names = []
        allocated_list_names = []
        for item in self.get_list_imported_names():
            original_list_names.append(item[0])

        for item in self.read_cache():
            for item_tuple in item:
                allocated_list_names.append(item_tuple[1])

        list_unallocated = self.personel_allocation.get_unallocated(
            allocated_list_names, original_list_names)
        return list_unallocated

    def get_list_imported_names(self):
        """Retrieves a list of imported names from a file"""
        parser = FileParser(
            os.path.dirname(os.path.realpath("filepath")) + "/input.txt")
        input_list = parser.read_file()
        return input_list

    def read_cache(self):
        with open('cache') as f:
            contents = f.read()
            return ast.literal_eval(contents)
