map_table = [[],
             [],
             []]
#prend un caractere
#renvoi un nombre sous forme de caractere
def num_from_char(char):
    ascii_value = ord(char)
    if ascii_value >= 48 and ascii_value <= 57:
        return str(ascii_value - 48)
    elif ascii_value >= 65 and ascii_value <= 90:
        return str(ascii_value - 65 + 10)
    elif ascii_value >= 97 and ascii_value <= 122:
        return str(ascii_value - 97 + 36)
    else:
        raise ValueError()

#prend un string
#renvoi un nombre sous forme de caractere
def num_from_string(string):
    out_put_string = ''
    for char in string:
        out_put_string += num_from_char(char)
    return out_put_string

#prend un nombre sous forme de string
#renvoi un caractere
def char_from_num(number):
    int_number = int(number)
    if int_number < 0 or int_number > 62:
        raise ValueError()
    elif int_number <= 9:
        return str(unichr(int_number + 48))
    elif int_number <= 35:
        return str(unichr(int_number + 65 - 10))
    elif int_number <= 61:
        return str(unichr(int_number + 97 - 36))

def consecutive_pair(number):
    pos = 0
    length =  len(number)
    while pos < length:
        if length - pos >= 2:
            if int(number[pos]) == 0 or int(number[pos]) >= 6:
                pair = number[pos:pos+1]
                pos += 1
            else:
                pair = number[pos:pos+2]
                pos += 2
        else:
            pair = number[pos:pos+1]
            pos += 1
        yield pair


#prend un nombre sous forme de string
#renvoi un string
def string_from_num(number):
    out_put_string = ''
    if len(number) == 0:
        return ValueError()
    for val in  consecutive_pair(number):
        out_put_string += char_from_num(val)
    return out_put_string

for val in consecutive_pair('70608090123456'):
    print val
