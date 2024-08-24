import pyls
import time
import os


def test_filename():
    """
    tests pyls.filename function
    """
    info1 = {"filename": "cats_and_dogs.txt", "isdir": False, "isexecfile": False}
    info2 = {"filename": "cats_and_dogs2", "isdir": False, "isexecfile": True}
    info3 = {"filename": "myfiles", "isdir": True, "isexecfile": False}
    assert pyls.filename(info1, False) == "cats_and_dogs.txt"
    assert pyls.filename(info1, True) == "cats_and_dogs.txt"
    assert pyls.filename(info2, False) == "cats_and_dogs2"
    assert pyls.filename(info2, True) == "cats_and_dogs2*"
    assert pyls.filename(info3, False) == "myfiles"
    assert pyls.filename(info3, True) == "myfiles/"


def test_detailed_view():
    """
    tests pyls.detailed_view
    """
    epoch = time.localtime(0)
    info1 = {
        "filename": "cats_and_dogs.txt",
        "isdir": False,
        "isexecfile": False,
        "filesize": 0,
        "modtime": epoch,
    }
    info2 = {
        "filename": "cats_and_dogs2",
        "isdir": False,
        "isexecfile": True,
        "filesize": 312856782,
        "modtime": epoch,
    }
    assert (
        pyls.detailed_view(info1, True)
        == "1970-01-01 05:30:00            0 cats_and_dogs.txt"
    )
    assert (
        pyls.detailed_view(info2, True)
        == "1970-01-01 05:30:00    312856782 cats_and_dogs2*"
    )
    assert (
        pyls.detailed_view(info2, False)
        == "1970-01-01 05:30:00    312856782 cats_and_dogs2"
    )


def with_file_fixture(tests):
    # Setup
    with open("testfile", "w") as f:
        f.write("sample data")
    path = "./testfile"
    os.utime(path, times=(0, 0))
    expected = {
        "path": path,
        "filename": "testfile",
        "isdir": False,
        "isexecfile": False,
        "filesize": 11,
        "modtime": time.localtime(0.0),
    }

    # Tests
    try:
        tests(expected)
    finally:
        # Teardown
        os.remove(path)


def _file_info_tests(expected):
    info = pyls.file_info(".", expected["filename"])
    assert info["path"] == expected["path"]
    assert info["filename"] == expected["filename"]
    assert info["isdir"] == expected["isdir"]
    assert info["isexecfile"] == expected["isexecfile"]
    assert info["filesize"] == expected["filesize"]
    assert info["modtime"] == expected["modtime"]


def test_file_info():
    with_file_fixture(_file_info_tests)
