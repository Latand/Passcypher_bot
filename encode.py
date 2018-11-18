from secret import key_func
import random
from messages import to_mix

# Sorry for some obfuscation, but you'll easily reverse it if you want :)


def char_mixer(____):
    _ = []
    _____ = []
    for i in range(len(____)):
        __ii__ = to_mix
        __i__ = ""
        _i_ = random.randint(1, 8)
        ___i__ = random.randint(0, 1)
        _.extend(str(_i_))
        for _iii_ in range(_i_):
            __i__ += __ii__[random.randint(1, len(__ii__)-1)]
            if ___i__:
                __i__ = __i__.upper()
            else:
                __i__ = __i__.lower()
        _____.append(f"{____[i]}{__i__}")
    return "".join(_____), int("".join(_))


def code_lock(master_pass, raw_code):

    new_key = key_func(master_pass)
    locked_code = raw_code * new_key
    return locked_code


def encode(to_encrypt, master_pass):

    result, raw_code = char_mixer(to_encrypt)
    code = code_lock(master_pass, raw_code)

    return result, code
