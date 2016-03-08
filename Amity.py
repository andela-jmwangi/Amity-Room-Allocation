"""
This shows the usage and options that available for the Amity room allocation app
Usage:
    amity allocate  [(-p <pathtofile>)]
    amity viewallocations  [(-r <nameofroom>) (-t <categoryofroom>)]
    amity viewunallocated  [(-r <nameofroom>) (-t <categoryofroom>)]
    amity (-s | --start)
    amity (-h | --help | --version)
Options:
    -s, --start Starts the program
    -h, --help  Shows a list of commands and their usage
"""


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
    file = None

    @parser
    def do_allocaterooms(self, arg):
        """Usage: allocate  [(-p <pathtofile>)]"""

        allocateroom(arg)

    @parser
    def do_viewallocations(self, arg):
        """Usage: [(-r <nameofroom>) (-t <categoryofroom>)]"""

        viewallocations(arg)

    def do_quit(self, arg):
        """Exit application."""

        print('Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])