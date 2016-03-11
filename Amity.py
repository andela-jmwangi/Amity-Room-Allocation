#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This shows the usage and options that available for Amity room allocation app
Usage:
    amity allocaterooms
    amity viewallocations  [(-r <nameofroom>)]
    amity viewunallocated
    amity (-s | --start)
    amity (-h | --help | --version)
Options:
    -s, --start  Starts the program.
    -h, --help  Shows a list of commands and their usage.
"""

from Tkinter import Tk
import tkFileDialog
from tkFileDialog import askopenfilename
import sys
import cmd
from docopt import docopt, DocoptExit
from colorama import init, Fore, Back, Style
from termcolor import cprint
from pyfiglet import figlet_format
from utils.Fileparser import Fileparser
from db.DatabaseManager import DatabaseManager
from random import randint
from utils.Allocations import Allocations
from models.Rooms import Rooms
from clint.textui import colored, puts, indent
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from colorama import init, Fore, Back, Style


# compares the arguments to determine if all have been entered in correct
# manner


def parser(func):

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


"""Class overrides method parser so as to validate input.The input arguments
    are mapped to respective methods
"""


class Amity (cmd.Cmd):

    prompt = '(Amity): '

    @parser
    def do_allocaterooms(self, arg):
        """Usage: allocate """

        allocaterooms(arg)

    def quit(self):
        self.root.destroy

    @parser
    def do_viewallocations(self, arg):
        """Usage: viewallocations [(-r <nameofroom>)]"""

        viewallocations(arg)

    @parser
    def do_viewunallocated(self, arg):
        """Usage: viewunallocated """

        viewunallocated(arg)

    def do_quit(self, arg):
        """Exit application."""

        print('Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

"""Allocates staff to rooms based on file contents
"""


def viewallocations(docopt_args):
    rooms = Rooms()
    db = DatabaseManager("Amity.sqlite")
    allocations = Allocations("")
    if docopt_args["-r"]:
        specific_room = docopt_args["<nameofroom>"]
        print("\n" + Back.GREEN + specific_room +
              " (" + rooms.get_room_type(specific_room) + ")" + Back.RESET)
        cursor = db.query(
            "SELECT * from Allocations where Room_name = '" + specific_room + "'")
        for row in cursor:
            personnel_name = row[1]
            personnel_type = row[4]
            print Fore.YELLOW + personnel_name + ", ",
        print "\n" + Fore.RESET
    else:
        list_rooms = allocations.getalloccupiedrooms()
        for room in list_rooms:
            print("\n" + Back.GREEN + room +
                  " (" + rooms.get_room_type(room) + ")" + Back.RESET)
            cursor = db.query(
                "SELECT * from Allocations where Room_name = '" + room + "'")
            for row in cursor:
                personnel_name = row[1]
                personnel_type = row[4]
                print Fore.YELLOW + personnel_name + ", ",

            print "\n" + Fore.RESET


def viewunallocated(docopt_args):
    allocations = Allocations("")
    unallocated = allocations.unallocated()
    if len(unallocated) > 0:
        print "Unallocated persons: "
        for name in unallocated:
            print name + " ,",
        print "\n"
    else:
        print "No unallocated people found."


def allocaterooms(docopt_args):
    root = Tk()
    root.withdraw()
    root.update()
    file = tkFileDialog.askopenfile(
        parent=root, mode='rb', title='Choose a file')
    if file:
        # savefile path for future use
        savefilepath(file.name)
        # read file to get list
        parser = Fileparser(file.name)
        inputlist = parser.readfile()
        allocation = Allocations(inputlist)
        allocations_list = allocation.allocate()
        if len(allocations_list) > 0:
            puts(colored.green(str(len(allocations_list)) +
                             " people allocated successfully. Do you wish to view them? (y)(n)"))
            answer = raw_input(">")
            if answer == "y":
                dict = {}
                for item in allocations_list:
                    for item2 in item:
                        if item2[0] in dict:
                            dict[item2[0]].append(item2[1])
                        else:
                            dict[item2[0]] = []
                            dict[item2[0]].append(item2[1])

                for room_name,occupants in dict.iteritems():
                    puts(colored.green(room_name))
                    print ",".join(occupants)
                    print "\n"
            else:
                return

    else:
        print("You did not select a file")
    root.destroy()


def savefilepath(path):
    with open("filepath", "w") as text_file:
        text_file.write(path)


def showwelcomemsg():
    init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
    cprint(figlet_format('Amity', font='starwars'),
           'green', attrs=['bold'])
    print(Back.RED + 'Welcome to Amity Room Allocation!' + Back.RESET +
          Style.DIM + '\n(type help for a list of commands.)' + Style.NORMAL)


"""starts application when -start is specified
"""

if opt['--start']:

    showwelcomemsg()
    Amity().cmdloop()  # creates the REPL

print(opt)
