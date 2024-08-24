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
parser.add_argument(
    "-F",
    "--filetype",
    help="Shows a file type indicator character for directories and executable files.",
    action="store_true",
)
args = parser.parse_args()


def main(args):
    list_directory(args.dirname, args.filetype)


def list_directory(dirname, show_filetype):
    """
    Prints contents of given directory to stdout, according to the other flags.

    :param dirname: The directory name whose contents are to be printed.
    :param show_filetype: Boolean indicating whether a filetype indicator
        character is to be appended to the printed file names.
    """
    dircontents = get_dir_contents(dirname)
    display_dir_contents(dircontents, show_filetype)


def get_dir_contents(dirname):
    """
    Returns a list of items describing the contents of the directory.
    In this case, the return is a list of strings giving the file names.
    """
    assert os.path.isdir(
        dirname
    ), f"Directory {dirname} does not exist or is not a directory."

    return [file_info(dirname, f) for f in os.listdir(dirname)]


def file_info(dirname, filename):
    assert os.path.isdir(dirname)

    path = os.path.join(dirname, filename)
    return {
        "filename": filename,
        "isdir": os.path.isdir(path),
        "isexecfile": os.access(path, os.X_OK) and not os.path.isdir(path),
    }


def display_dir_contents(dircontents, show_filetype):
    """
    Takes a list of dir entry descriptions as provided by
    `get_dir_contents` and shows them one per line.

    :param dircontents: A list of dictionaries of the form returned
        by `file_info`.
    """
    for info in dircontents:
        print(filename(info, show_filetype))


def filename(info, show_filetype):
    return info["filename"] + (filetype_char(info) if show_filetype else "")


def filetype_char(info):
    """
    :param info: As returned by `file_info`
    :returns: '/' if the entity is a directory, and '*' if it is
       an executable file and '' in other cases.
    """
    ch = ""
    if info["isdir"]:
        ch += "/"
    if info["isexecfile"]:
        ch += "*"
    return ch


if __name__ == "__main__":
    main(args)
