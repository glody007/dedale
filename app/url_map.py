#prend un caractere
#renvoi un nombre sous forme de caractere
def num_from_char(char):
    ascii_value = ord(char)
    if ascii_value >= 48 and ascii_value <= 57:
        return str(ascii_value - 48 + 1)
    elif ascii_value >= 65 and ascii_value <= 90:
        return str(ascii_value - 65 + 11)
    elif ascii_value >= 97 and ascii_value <= 122:
        return str(ascii_value - 97 + 37)
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
    elif int_number <= 10:
        return str(unichr(int_number+ 48 - 1))
    elif int_number <= 36:
        return str(unichr(int_number + 65 - 11))
    elif int_number <= 62:
        return str(unichr(int_number + 97 - 37))

def consecutive_pair(number):
    pos = 0
    length =  len(number)
    while pos < length:
        if length - pos >= 2:
            pair = number[pos:pos+2]
        else:
            pair = number[pos:pos+1]
        yield pair
        pos += 2


#prend un nombre sous forme de string
#renvoi un string
def string_from_num(number):
    out_put_string = ''
    if len(number) == 0:
        return ValueError()
    for val in  consecutive_pair(number):
        out_put_string += char_from_num(val)
    return out_put_string

print string_from_num('1234567')
print num_from_string('BXt6')