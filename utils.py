def gather_city_and_code(string):
    splitted = string.split('(')
    return splitted[0], splitted[1][:-1]
