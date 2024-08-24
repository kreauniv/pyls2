import os
import argparse

parser = argparse.ArgumentParser(
    prog="pyls", description="Lists the contents of the given directory."
)
parser.add_argument(
    "dirname",
    help="The directory to list. Defaults to the current directory.",
    nargs="?",
    default=".",
)
args = parser.parse_args()


def main(args):
    list_directory(args.dirname)


def list_directory(dirname):
    """ """
    dircontents = get_dir_contents(dirname)
    display_dir_contents(dircontents)


def get_dir_contents(dirname):
    """
    Returns a list of items describing the contents of the directory.
    In this case, the return is a list of strings giving the file names.
    """
    return os.listdir(dirname)


def display_dir_contents(dircontents):
    """
    Takes a list of dir entry descriptions as provided by
    `get_dir_contents` and shows them one per line.
    """
    for item in dircontents:
        print(item)


if __name__ == "__main__":
    main(args)
