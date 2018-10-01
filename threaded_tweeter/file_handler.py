import os


def load_thread_file(path):
    """
    :type path: str, either relative or absolute to current cwd
    :rtype: str, unparsed input thread
    """
    with open(path, "r") as f:
        return ''.join(f.readlines())

def load_media_file(path):
    return open(path, "rb")
