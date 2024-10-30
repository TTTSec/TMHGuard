import platform


def get_os():

   return platform.system()

def get_os_expanded():
    return platform.version()


def get_release_version():
    return platform.release()

def get_os_detailed():
    return platform.platform()

