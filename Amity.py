#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This shows the usage and options that available for Amity room allocation app
Usage:
    amity allocaterooms
    amity viewallocations  [(-r <name_of_room>)]
    amity viewunallocated
    amity unallocate (-p <fname> <lname> -r <name_of_room>)
    amity reset
    amity (-s | --start)
    amity (-h | --help | --version)
Options:
    -s, --start  Starts the program.
    -h, --help  Shows a list of commands and their usage.
"""

from Tkinter import Tk
import tkFileDialog
import sys
import cmd
from docopt import docopt, DocoptExit
from colorama import init, Fore, Back, Style
from termcolor import cprint
from pyfiglet import figlet_format
from utils.Fileparser import Fileparser
from db.DatabaseManager import DatabaseManager
from utils.Allocations import Allocations
from models.Rooms import Rooms
from clint.textui import colored, puts


def parser(func):
    """compares args to determine if all have been entered in correct manner"""

    def fn(self, arg):
        try:
            # tries to compare entered commands against the doc
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The entered arguments don't match

            print('Sorry,you entered an invalid command')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Amity (cmd.Cmd):

    """Class overrides method parser so as to validate input.The input arguments
    are mapped to respective methods """

    prompt = '(Amity): '

    @parser
    def do_allocaterooms(self, arg):
        """Usage: allocate """

        allocate_rooms(arg)

    def quit(self):
        self.root.destroy

    @parser
    def do_viewallocations(self, arg):
        """Usage: viewallocations [(-r <name_of_room>)]"""

        view_allocations(arg)

    @parser
    def do_unallocate(self, arg):
        """Usage: unallocate (-p <fname> <lname> -r <name_of_room>)"""

        unallocate(arg)

    @parser
    def do_viewunallocated(self, arg):
        """Usage: viewunallocated """

        view_unallocated(arg)

    @parser
    def do_reset(self, arg):
        """Usage: reset """

        reset(arg)

    def do_quit(self, arg):
        """Exit application."""

        print('Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])


def reset(docopt_args):
    """Resets all allocations"""

    puts(colored.green("Are you sure you want to reset allocations? (y)(n)"))
    answer = raw_input(">")
    if answer == "y" or answer == "Y":
        db = DatabaseManager("Amity.sqlite")
        db.query("DROP TABLE Allocations")
        db.query("DROP TABLE Rooms")
        db.query("DROP TABLE Staff")
        puts(colored.green("Allocations reset successfully!"))


def unallocate(docopt_args):
    """Unallocates a staff his/her given room"""

    personnel_name = ""
    name_of_room = ""
    if docopt_args["-p"] and docopt_args["-r"]:
        personnel_name = docopt_args["<fname>"] + " " + docopt_args["<lname>"]
        name_of_room = docopt_args["<name_of_room>"]
        db = DatabaseManager("Amity.sqlite")
        # query db to find the apecific allocation
        cursor = db.query("DELETE from Allocations where Personnel_Name = '" +
                          personnel_name + "' and Room_name = '" + name_of_room + "'")
        if cursor.rowcount > 0:
            puts(colored.green(
                personnel_name + " has been unnallocated room " + name_of_room + " successfully!"))
            # update to cache
            f = open("cache", 'r')
            filedata = f.read()
            f.close()
            newdata = filedata.replace(
                "('" + name_of_room + "', '" + personnel_name + "')", "")
            f = open("cache", 'w+')
            f.write(newdata)
            f.close()

        else:
            puts(colored.red("The allocation does not exist"))
    else:
        puts(colored.red("You failed to supply peronnel name and room name"))


def view_allocations(docopt_args):
    """Allocates staff to rooms based on file contents"""

    rooms = Rooms()
    db = DatabaseManager("Amity.sqlite")
    allocations = Allocations("")
    if docopt_args["-r"]:
        specific_room = docopt_args["<name_of_room>"]
        print("\n" + Back.WHITE + Fore.RED + specific_room +
              " (" + rooms.get_room_type(specific_room) + ")" + Back.RESET + Fore.RESET)
        cursor = db.query(
            "SELECT * from Allocations where Room_name = '" + specific_room + "'")
        if len(cursor.fetchall()) > 0:
            cursor2 = db.query(
                "SELECT * from Allocations where Room_name = '" + specific_room + "'")
            for row in cursor2:
                personnel_name = row[1]
                print Fore.GREEN + personnel_name + ", ",
        else:
            puts(colored.red("No allocations for this room"))
        print "\n" + Fore.RESET
    else:
        list_rooms = allocations.getalloccupiedrooms()
        for room in list_rooms:
            print("\n" + Back.WHITE + Fore.RED + room +
                  " (" + rooms.get_room_type(room) + ")" + Back.RESET + Fore.RESET)
            cursor = db.query(
                "SELECT * from Allocations where Room_name = '" + room + "'")
            for row in cursor:
                personnel_name = row[1]
                print Fore.GREEN + personnel_name + ", ",

            print "\n" + Fore.RESET


def view_unallocated(docopt_args):
    allocations = Allocations("")
    unallocated = allocations.unallocated()
    if len(unallocated) > 0:
        puts(colored.green("Unallocated persons: "))
        for name in unallocated:
            print name + " ,",
        print "\n"
    else:
        print "No unallocated people found."


def allocate_rooms(docopt_args):
    root = Tk()
    root.withdraw()
    root.update()
    file = tkFileDialog.askopenfile(
        parent=root, mode='rb', title='Choose a file')
    if file:
        # savefile path for future use
        save_file_path(file.name)
        # read file to get list
        parser = Fileparser(file.name)
        inputlist = parser.readfile()
        allocation = Allocations(inputlist)
        allocations_list = allocation.allocate()
        if len(allocations_list) > 0:
            puts(colored.green(str(len(allocations_list)) +
                               " people allocated successfully. Do you wish to view them? (y)(n)"))
            answer = raw_input(">")
            # allow user to view allocated people
            if answer.lower() == "y":
                allocation_map = {}
                # loop through list of allocations
                for item in allocations_list:
                    for item2 in item:
                        if item2[0] in allocation_map:
                            allocation_map[item2[0]].append(item2[1])
                        else:
                            allocation_map[item2[0]] = []
                            allocation_map[item2[0]].append(item2[1])

                for room_name, occupants in allocation_map.iteritems():
                    puts(colored.green(room_name))  # prints room name
                    print ",".join(occupants)  # prints occupants in the room
                    print "\n"
            else:
                return

    else:
        print("You did not select a file")
    root.destroy()


def save_file_path(path):
    with open("filepath", "w+") as text_file:
        text_file.write(path)


def show_welcome_msg():
    init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
    cprint(figlet_format('Amity', font='starwars'),
           'green', attrs=['bold'])
    print(Back.RED + 'Welcome to Amity Room Allocation!' + Back.RESET +
          Style.DIM + '\n(type help for a list of commands.)' + Style.NORMAL)


if opt['--start']:
    """starts application when -start is specified"""

    show_welcome_msg()
    Amity().cmdloop()  # creates the REPL

print(opt)
