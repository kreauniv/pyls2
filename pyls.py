import os
import argparse
import time

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
parser.add_argument(
    "-l",
    "--long-format",
    help="Shows file modification time and size in a tabular format.",
    action="store_true",
)
args = parser.parse_args()


def main(args):
    list_directory(args.dirname, args.filetype, args.long_format)


def list_directory(dirname, show_filetype, show_details):
    """
    Prints contents of given directory to stdout, according to the other flags.

    :param dirname: The directory name whose contents are to be printed.
    :param show_filetype: Boolean indicating whether a filetype indicator
        character is to be appended to the printed file names.
    """
    dircontents = get_dir_contents(dirname)
    display_dir_contents(dircontents, show_filetype, show_details)


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
    """
    :param dirname: Name of directory of the file.
    :param filename: The file within the given directory.
    :returns: A dictionary containing details about the file.

        {
            "path": .. full path,
            "filename": .. same as `filename`,
            "isdir": .. bool indicating whether it is a directory,
            "isexecfile": .. bool indicating whether it is an executable *file*,
            "filesize": .. size of the file in bytes, or 0 if a directory,
            "modtime": .. `time` object giving the modification time in local TZ.
        }
    """
    assert os.path.isdir(dirname)

    path = os.path.join(dirname, filename)
    isdir = os.path.isdir(path)
    mtime_ts = os.path.getmtime(path)
    mtime = time.localtime(mtime_ts)
    return {
        "path": path,
        "filename": filename,
        "isdir": isdir,
        "isexecfile": os.access(path, os.X_OK) and not isdir,
        "filesize": os.path.getsize(path) if not isdir else 0,
        "modtime": mtime,
    }


def display_dir_contents(dircontents, show_filetype, show_details):
    """
    Takes a list of dir entry descriptions as provided by
    `get_dir_contents` and shows them one per line.

    :param dircontents: A list of dictionaries of the form returned
        by `file_info`.
    """
    for info in dircontents:
        if show_details:
            print(detailed_view(info, show_filetype))
        else:
            print(filename(info, show_filetype))


def filename(info, show_filetype):
    """
    Takes a `file_info` returned dictionary and returns the filename
    field optionally suffixed by a file type indicator character.

    :param info: A dictionary as returned by `file_info`
    :param show_filetype: A boolean indicating whether to append a type descriptor character.

    :returns: String which is the file name, but suffixed with a type character --
        '*' for executable files and '/' for directories.
    """
    return info["filename"] + (filetype_char(info) if show_filetype else "")


def detailed_view(info, show_filetype):
    """
    Formats a line of output in the "long format" as a string that can
    be printed out as is.

    :param info: A dictionary as returned by `file_info`
    :param show_filetype: Whether to append a filetype descriptor to the name.
    :returns: A formatted string giving details about the file.
    """
    fname = filename(info, show_filetype)
    t = info["modtime"]
    sz = info["filesize"]
    line = f"{t.tm_year}-{t.tm_mon:>02}-{t.tm_mday:>02} {t.tm_hour:>02}:{t.tm_min:>02}:{t.tm_sec:>02} {sz:>12} {fname}"
    return line


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
