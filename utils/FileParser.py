
class FileParser(object):
    """This class reads the file input and returns appropriate data to caller"""

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def read_file(self):
        """Read file contents and return a list"""
        # ipdb.set_trace(context=1)
        list_allocations = []
        contents = [line.rstrip('\n') for line in open(self.path_to_file, 'r')]
        for line in contents:
            words = line.split(" ")
            person_name = words[0].replace(
                "'", "") + " " + words[1].replace("'", "")
            person_type = words[2]
            residing = "N"
            if len(words) == 4:
                residing = "Y"
            list_allocations.append([person_name, person_type, residing])
        return list_allocations
