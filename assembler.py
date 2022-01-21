#!/usr/bin/env python3

# ^^ Linux-executable init


def to_bin(number: str, special=False):
    if special:
        if number[0] == 'x':
            r = format(int(number[1:], 16), '016b')
        elif number[0] == 'b':
            r = format(int(number[1:], 2), '016b')
        else:
            r = format(int(number[1:], 10), '016b')
        s = ''
        for i in range(len(r)):
            s += r[i]
            if i % 4 == 3 and i + 1 != len(r):
                s += ' '
        return s + '\n'
    if number[0] == 'x':
        return format(int(number[1:3], 16), '04b')
    elif number[0] == 'b':
        return format(int(number[1:3], 2), '04b')
    else:
        return format(int(number[0:2], 10), '04b')


def assemble(text):
    r = ''
    a = ' '
    b = '\n'
    lines = text.split('\n')
    for i in range(len(lines)):
        parts = lines[i].split(a)
        if lines[i] == '' or lines[i][0] == '#' or lines[i] == '\n':
            pass
        elif 'if' in parts:
            if '=' in parts:
                r += '1011 ' + to_bin(parts[1]) + a + to_bin(parts[3]) + a + to_bin(parts[5]) + b
            elif '>' in parts:
                r += '1100 ' + to_bin(parts[1]) + a + to_bin(parts[3]) + a + to_bin(parts[5]) + b
            elif '<' in parts:
                r += '1101 ' + to_bin(parts[1]) + a + to_bin(parts[3]) + a + to_bin(parts[5]) + b
            else:
                raise SyntaxError()
        elif '=' not in parts:
            if parts[0] == 'pass':
                r += '0000 0000 0000 0000\n'
            elif parts[0] == 'jump':
                r += '0000 0000 0001 ' + to_bin(parts[1]) + b
            elif parts[0] == 'set':
                r += to_bin(parts[1], True)
            elif parts[0] == 'end':
                r += '0000 0000 0000 1111\n'
            else:
                raise SyntaxError()
        elif parts[1] == '=' and len(parts) == 3:
            r += '0000 0001 ' + to_bin(parts[2]) + a + to_bin(parts[0]) + b
        elif parts[3] == 'and':
            r += '1000 ' + to_bin(parts[2]) + a + to_bin(parts[4]) + a + to_bin(parts[0]) + b
        elif parts[3] == 'or':
            r += '1001 ' + to_bin(parts[2]) + a + to_bin(parts[4]) + a + to_bin(parts[0]) + b
        elif parts[3] == 'xor':
            r += '1010 ' + to_bin(parts[2]) + a + to_bin(parts[4]) + a + to_bin(parts[0]) + b
        elif parts[3] == '+':
            r += '1110 ' + to_bin(parts[2]) + a + to_bin(parts[4]) + a + to_bin(parts[0]) + b
        elif parts[3] == '-':
            r += '1111 ' + to_bin(parts[2]) + a + to_bin(parts[4]) + a + to_bin(parts[0]) + b
        elif parts[2] == 'ls':
            r += '0000 0100 ' + to_bin(parts[3]) + a + to_bin(parts[0]) + b
        elif parts[2] == 'rs':
            r += '0000 0101 ' + to_bin(parts[3]) + a + to_bin(parts[0]) + b
        elif parts[2] == 'not':
            r += '0000 0110 ' + to_bin(parts[3]) + a + to_bin(parts[0]) + b
        elif parts[2] == 'lt':
            r += '0000 1100 ' + to_bin(parts[3]) + a + to_bin(parts[0]) + b
        elif parts[2] == 'rt':
            r += '0000 1101 ' + to_bin(parts[3]) + a + to_bin(parts[0]) + b
        elif parts[2] == 'get':
            if parts[3] == 'next':
                r += '0000 0000 0010 ' + to_bin(parts[0]) + b
            else:
                r += '0000 0010 ' + to_bin(parts[3]) + a + to_bin(parts[0]) + b
        elif parts[0] == 'set':
            r += '0000 0011 ' + to_bin(parts[1]) + a + to_bin(parts[3]) + b
        else:
            raise SyntaxError
    return r


def main():
    input_file = input('Input file: ')
    export_file = input('Export file: ')
    with open(input_file, 'r') as f:
        code = assemble(f.read())
    with open(export_file, 'w') as f:
        f.write(code)


if __name__ == '__main__':
    main()
