at_least_one = False

def compare_char(regex: str, character: str):
    """ Compare one character regex expression against a character"""
    if not regex:
        return True
    elif not character:
        return False
    return regex == '.' or regex == character

def compare_beginning(regex: str, string: str):
    """ Compare a regex expression against the beginning of a string"""
    # base case
    if not regex:
        return True
    elif not string:
        return False

    # input validation
    if len(regex) > 1:
        if regex[1] == '?':
            if compare_char(regex[0], string[0]):
                return compare_beginning(regex[2:], string[1:])
            else:
                return compare_beginning(regex[2:], string)
        elif regex[1] == '+':
            global at_least_one
            if regex[0] == '.' and at_least_one:
                if len(regex) > 2:
                    return regex[2] in string
                else:
                    return True

            if compare_char(regex[0], string[0]):
                at_least_one = True
                return compare_beginning(regex, string[1:])
            else:
                return compare_beginning(regex[2:], string) and at_least_one
        elif regex[1] == '*':
            if regex[0] == '.':
                if len(regex) > 2:
                    return regex[2] in string
                else:
                    return True

            if compare_char(regex[0], string[0]):
                return compare_beginning(regex,string[1:])
            else:
                return compare_beginning(regex[2:], string)

    return compare_char(regex[0], string[0]) and compare_beginning(regex[1:], string[1:])

def compare_anywhere(regex: str, string: str):
    """ Compare a regex expression against any part of a string """
    # base case
    if regex and not string:
        return False
    elif not regex and not string:
        return True

    return compare_beginning(regex, string) or compare_anywhere(regex, string[1:])

def entry_point(regex: str, string: str):
    """ Select the correct comparison to make"""
    if regex: # if the regex is empty it's always True
        if regex[0] == '^' and regex[-1] == '$':
            return compare_beginning(regex[1:-1], string) and compare_ending(regex[1:-1], string)
        elif regex[0] == '^': # compares only against the beginning of the string
            return compare_beginning(regex[1:], string)
        elif regex[-1] == '$': # compares only the regex against the ending of the string
            return compare_ending(regex[:-1], string)
        else:
            return compare_anywhere(regex, string)
    else:
        return True

def compare_ending(regex, string):
    """ Compare a regex expression against the ending of a string"""
    # base case
    if not regex:
        return True
    elif not string:
        return False

    # input validation
    if len(regex) > 1:
        if regex[-1] == '?':
            if compare_char(regex[-2], string[-1]):
                return compare_ending(regex[:-2], string[:-1])
            else:
                return compare_ending(regex[:-2], string)
        elif regex[-1] == '+':
            global at_least_one
            
            if at_least_one and regex[-2] == '.':
                if len(regex) > 2:
                    return regex[-3] in string
                else:
                    return True

            if compare_char(regex[-2], string[-1]):
                at_least_one = True
                return compare_ending(regex, string[:-1])
            else:
                return compare_ending(regex[:-3], string) and at_least_one
        elif regex[-1] == '*':            
            if regex[-2] == '.':
                if len(regex) > 2:
                    return regex[-3] in string
                else:
                    return True

            if compare_char(regex[-2], string[-1]):
                return compare_ending(regex,string[:-1])
            else:
                return compare_ending(regex[:-3], string)

    return compare_char(regex[-1], string[-1]) and compare_ending(regex[:-1], string[:-1])



regexp, input_string = input().split('|')

#test_cases = [('colou?r','color'), ('colou?r','colour'), ('colou?r','colouur'), ('colou*r','color'),
#              ('colou*r','colour'), ('colou*r','colouur'), ('col.*r','color'), ('col.*r','colour'), ('col.*r','colr'),
#              ('col.*r','collar'), ('col.*r$','colors'), ('colou+r','color'), ('colou+r','colour'),
#              ('colou+r','colouuur'),('col.*r$','colors'), ('col.*ur', 'color'), ('col.+ur', 'color'),
#              ('col.+r', 'color'), ('le$','apple'), ('^no+pe$','noooooope'), ('^apple$','apple'), ('^n.+pe$','noooooope')]
#
#expected_results = [True, True, False, True, True, True, True, True, True, True, False, False, True, True, False,
#                    False, False, True, True, True, True, True]
#
#for i, (key, value) in  enumerate(test_cases):
#    print(f"{key}:{value}", entry_point(key, value), expected_results[i])

print(entry_point(regexp, input_string))






