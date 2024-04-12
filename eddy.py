import sys
import re

def get_commands():
    n = False
    command = ""
    for arg in sys.argv[1:]:
        if (arg == '-n'):
            n = True
        else:
            command = arg
    return n, command


def parse_command(arg):
    chars = list(arg)
    line_num = -1
    pattern = ""
    if (chars[len(chars) - 1] == 'q'):
        if (chars[0] == "/"):
            pattern = arg[1:-2]
        else:
            line_num = int(arg[0:-1])
        return "quit", line_num, pattern.strip()
    elif (chars[len(chars) - 1] == 'p'):
        if (chars[0] == "/"):
            pattern = arg[1:-2]
        else:
            if (len(chars) == 1):
                line_num = 0
            else:
                line_num = int(arg[0:-1])
        return "print", line_num, pattern.strip()

def quit(line_num, pattern):
    for count, line in enumerate(sys.stdin):
        if (line_num != -1):
            if ((count + 1) <= line_num):
                print(line, end="")
            else:
                break
        elif (pattern != ""):
            print(line, end="")
            if (re.search(pattern, line)):
                break

def print_ln(line_num, pattern):
    for count, line in enumerate(sys.stdin):
        print(line, end="")
        if (line_num == 0):
            print(line, end="")
        elif (count == line_num - 1):
            print(line, end="")
        elif (pattern != ""):
            if (re.search(pattern, line)):
                print(line, end="")

def print_n(line_num, pattern):
    for count, line in enumerate(sys.stdin):
        if (count == line_num - 1):
            print(line, end="")
        elif (pattern != ""):
            if (re.search(pattern, line)):
                print(line, end="")

def main():
    n_flag, command_arg = get_commands()
    command, line_num, pattern = parse_command(command_arg)

    match command:
        case "quit":
            quit(line_num, pattern)
        case "print":
            if (n_flag):
                print_n(line_num, pattern)
            else:
                print_ln(line_num, pattern)

if __name__ == '__main__':
    main()

