import ast


def match_bracket(string, symbol):

    left_symbol = "{" if symbol == "}" else "["
    counter, pointer = 1, 0
    while counter:
        if string[pointer] == left_symbol:
            counter += 1
        elif string[pointer] == symbol:
            counter -= 1
        pointer += 1
    return pointer


def parse_dict(fbdict):

    new_dict = {}
    i, next, name = 0, 0, ""

    # parse string from the left
    while i < len(fbdict):

        # a dict starts
        if fbdict[i] == "{":
            next = i + 1 + match_bracket(fbdict[i + 1 :], "}")
            this_dict = fbdict[i + 1 : next + 1]
            if name == "":
                return parse_dict(this_dict)
            else:
                new_dict[name] = parse_dict(this_dict)

        # a list starts
        elif fbdict[i] == "[":
            next = i + 1 + match_bracket(fbdict[i + 1 :], "]")
            dict_list = []
            assert name == ""
            dct_start = i + 1
            while fbdict[dct_start] == "{":
                dct_end = dct_start + match_bracket(fbdict[dct_start + 1 :], "}")
                this_dict = fbdict[dct_start : dct_end + 1]
                dict_list.append(parse_dict(this_dict))
                dct_start = min(dct_end + 3, len(fbdict) - 1)
            new_dict = dict_list

        # => is the main key|value separator
        elif fbdict[i : i + 2] == "=>":
            # clean name from possible noise
            name = name.strip(' ,:"')

            # => points to dictionary
            if fbdict[i + 2] == "{":
                # isolate the dict and recur
                next = i + 3 + match_bracket(fbdict[i + 3 :], "}")
                new_dict[name] = parse_dict(fbdict[i + 3 : next + 1])
                next = min(next + 1, len(fbdict) - 1)

            # => points to list
            elif fbdict[i + 2] == "[":
                new_dict[name] = []
                # isolate the list
                next = i + 3 + match_bracket(fbdict[i + 3 :], "]")
                # will contain either values or dicts
                if fbdict[i + 3] != "{":
                    # just append [values]
                    new_dict[name] = ast.literal_eval(fbdict[i + 2 : next])
                else:
                    dct_start = i + 3
                    while fbdict[dct_start] == "{":
                        dct_end = dct_start + match_bracket(
                            fbdict[dct_start + 1 :], "}"
                        )
                        this_dict = fbdict[dct_start : dct_end + 1]
                        new_dict[name].append(parse_dict(this_dict))
                        dct_start = min(dct_end + 3, len(fbdict) - 1)
                next += 1

            # => points to values
            else:
                # key|value pairs separated by comma
                next = (
                    i + 2 + fbdict[i + 2 :].find('",')
                    if fbdict[i + 2] == '"'
                    else i + 2 + fbdict[i + 2 :].find(",")
                )
                # may be the last element
                if next < i + 2:
                    new_dict[name] = fbdict[i + 2 :].strip('"}')
                    next = len(fbdict) - 1
                else:
                    new_dict[name] = fbdict[i + 2 : next].strip('"}')
            # re-initialize
            name = ""

        # save key until => is found
        else:
            if type(fbdict) is list:
                return fbdict[i]
            else:
                name += fbdict[i]
            next = i
        # resume parsing
        i = next + 1

    return new_dict
