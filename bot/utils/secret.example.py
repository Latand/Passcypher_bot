# This is just the example, but it works


def key_func(__):
    return 13


def key_func_back(master, code):
    code = int(code)
    return str(code // 13)
