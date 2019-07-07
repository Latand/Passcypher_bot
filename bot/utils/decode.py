from bot.utils.secret import key_func_back
# Sorry for some obfuscation, but you'll easily reverse it if you want :)


def decode(master, password, code):
    original_code = key_func_back(master, code)

    decoded = [password[0]]
    _i___ = 1
    i___ = 0
    for _i in range(len(original_code)):
        while i___ < _i___ + int(original_code[_i]):
            i___ += 1
        try:
            decoded.append(password[i___])
        except:
            break
        _i___ = i___ + 1

    return "".join(decoded)
