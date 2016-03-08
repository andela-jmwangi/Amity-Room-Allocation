#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This shows the usage and options that available for Amity room allocation app
Usage:
    amity allocate  [(-p <file>)]
    amity viewallocations  [(-r <nameofroom>) (-t <categoryofroom>)]
    amity viewunallocated  [(-r <nameofroom>) (-t <categoryofroom>)]
    amity (-s | --start)
    amity (-h | --help | --version)
Options:
    -s, --start  Starts the program.
    -h, --help  Shows a list of commands and their usage.
"""

from Tkinter import Tk, Label
import tkFileDialog
from tkFileDialog import askopenfilename
import sys
import cmd
from docopt import docopt, DocoptExit
from colorama import init, Fore, Back, Style
from termcolor import cprint
from pyfiglet import figlet_format
from Fileparser import Fileparser
import easygui

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
        """Usage: allocate  [(-p <file>)]"""

        allocaterooms(arg)

    def quit(self):
        self.root.destroy

    @parser
    def do_viewallocations(self, arg):
        """Usage: [(-r <nameofroom>) (-t <categoryofroom>)]"""

        viewallocations(arg)

    def do_quit(self, arg):
        """Exit application."""

        print('Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

"""Allocates staff to rooms based on file contents
"""


def viewallocations(docopt_args):
    pass


def allocaterooms(docopt_args):
    root = Tk()
    root.withdraw()
    root.update()
    file  = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    if file:
        #read file to get list
        parser = Fileparser(file.name)
        inputlist = parser.getlinecontents()
        print inputlist
    else:
        print("You did not select a file")
    root.destroy()
    


def showwelcomemsg():
    init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
    # cprint(figlet_format('Amity', font='starwars'),
    #        'green', attrs=['blink'])
    print(Back.RED + 'Welcome to Amity Room Allocation!' + Back.RESET +
          Style.DIM + '\n(type help for a list of commands.)' + Style.NORMAL)


"""starts application when -start is specified
"""

if opt['--start']:
   

    showwelcomemsg()
    Amity().cmdloop()  # creates the REPL

print(opt)
