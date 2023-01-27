import ntpath
import os
import posixpath
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath


def dot_path(pathname):
    """Return path str that may start with '.' if relative.

    https://stackoverflow.com/a/72064941
    """
    if isinstance(pathname, str):
        pathname = Path(pathname)

    if not isinstance(pathname, PurePath):
        raise ValueError("Not a Path object")

    if pathname.is_absolute():
        return os.fsdecode(pathname)

    if isinstance(pathname, PureWindowsPath):
        return ntpath.join(".", pathname)

    if isinstance(pathname, PurePosixPath):
        return posixpath.join(".", pathname)

    return os.path.join(".", pathname)
