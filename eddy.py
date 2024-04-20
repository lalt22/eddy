import sys
import re
import typing

SUBSTITUTION_PATTERN = r'\A(/[^/]*/){0,1}\d*s\S(\[*[^\]/]*\]*)\S[\w\-/]*\Sg{0,1}'
QUIT_PATTERN = r'.*q\Z'
PRINT_PATTERN = r'.*p\Z'
DELETE_PATTERN = r'.*d\Z'
NUM_ADDR_PATTERN = r'\A\d*,{0,1}\d*\Z'
REGEX_ADDR_PATTERN = r'\A\S+\Z'

# def get_commands():
#     n = False
#     command = ""
#     for arg in sys.argv[1:]:
#         if (arg == '-n'):
#             n = True
#         else:
#             command = arg
#     return n, command


def get_commands():
    n = False
    commands = []
    for arg in sys.argv[1:]:
        if (arg == '-n'):
            n = True
        else:
            arg_commands = arg.split(';')
            for arg_command in arg_commands:
                commands.append(arg_command)
    return n, commands

def get_subst_patterns(arg):
    strs = arg.split("/")
    return strs

def get_addresses(arg, char):
    line_num = [-1]
    regex_addr = ""
    address = arg.split(char)
    if (re.match(NUM_ADDR_PATTERN, address[0])):
            line_num = address[0].split(",")
    elif (re.match(REGEX_ADDR_PATTERN, address[0])):
        regex_addr = address[0].replace('/', '')
    return line_num, regex_addr

# def get_relevant_line_nums(line_num):
#     lines = line_num.split(",")
#     return lines

def parse_command(arg):
    if (re.match(QUIT_PATTERN, arg)):
        line_num, regex_addr = get_addresses(arg, 'q')
        return "quit", line_num, regex_addr
    elif (re.match(PRINT_PATTERN, arg)):
        line_num, regex_addr = get_addresses(arg, 'p')
        return "print", line_num, regex_addr
    elif (re.match(DELETE_PATTERN, arg)):
        line_num, regex_addr = get_addresses(arg, 'd')
        return "delete", line_num, regex_addr
    elif (re.match(SUBSTITUTION_PATTERN, arg)):
        return "subst", [-1], ""


def last_line(itr: typing.Iterable[str]) -> typing.Tuple[bool, str]:
    last = None
    for line in itr:
        if last is not None:
            yield False, last
        last = line
    if last is not None:
        yield True, last


def quit(line_num, pattern):
    for count, line in enumerate(sys.stdin):
        if (line_num[0] != -1):
            if ((count + 1) <= int(line_num[0])):
                print(line, end="")
            else:
                break
        elif (pattern != ""):
            print(line, end="")
            if (re.search(pattern, line)):
                break

def print_ln(line_num, pattern):
    num_lines = len(line_num)
    for count, line in enumerate(last_line(sys.stdin)):
        if (pattern == '$'):
            if (line[0] == True):
                print(line[1], end="")
        if (num_lines > 1):
             if (count >= int(line_num[0]) - 1 and count <= int(line_num[1]) - 1):
                print(line[1], end="")
        if (num_lines == 1):
            if (line_num[0] == ""):
                print(line[1], end="")
            elif (count == int(line_num[0]) - 1):
                print(line[1], end="")
        if (pattern != ""):
            if (re.search(pattern, line[1])):
                print(line[1], end="")
        elif (line_num == -1):
           print(line[1], end="")
        
        print(line[1], end="")


def print_n(line_num, pattern):
    num_lines = len(line_num)
    for count, line in enumerate(last_line(sys.stdin)):
        if (pattern == '$'):
            if (line[0] == True):
                print(line[1], end="")
        elif (num_lines > 1):
             if (count >= int(line_num[0]) - 1 and count <= int(line_num[1]) - 1):
                print(line[1], end="")
        elif (num_lines == 1):
            if (count == int(line_num[0]) - 1):
                print(line[1], end="")
        elif (count == line_num - 1):
            print(line[1], end="")
        if (pattern != ""):
            if (re.search(pattern, line[1])):
                print(line[1], end="")

def delete(line_num, pattern):
    num_lines = len(line_num)
    for count, line in enumerate(last_line(sys.stdin)):
        if (pattern == '$'):
            if (line[0] == True):
                break
        if (num_lines > 1):
            if (count >= int(line_num[0]) - 1 and count <= int(line_num[1]) - 1):
                continue
        if (num_lines == 1):
            if (line_num[0] == ""):
                continue
            if (count == int(line_num[0]) -1):
                continue
        if (pattern != ""):
            if (re.search(pattern, line[1])):
                continue
        elif (line_num[0] == -1):
            break
        print(line[1], end="")



def substitute(re_addr, line_num, old, new, is_g):
    # print(line_num)
    num_lines = len(line_num)
    for count, line in enumerate(sys.stdin):
        #If only substutiting at num addr
        if (num_lines > 1):
            if (count >= int(line_num[0]) - 1 and count <= int(line_num[1]) - 1):
                get_and_sub_matches(line, old, new, is_g)
        
        elif (count == int(line_num[0]) - 1):
            get_and_sub_matches(line, old, new, is_g)
        #If only subbing at regexp addr
        elif (re_addr != ""):
            if (re.search(re_addr, line)):
                get_and_sub_matches(line, old, new, is_g)
            else:
                print(line, end="")
        elif (line_num[0] == -1):
            get_and_sub_matches(line, old, new, is_g)
        #If subbing all lines that contain the old regex
        
        #Not subbing
        else:
            print(line, end="")

def get_and_sub_matches(line, old, new, is_g):
    if (is_g):
        new_line = re.sub(old, new, line)
        print(new_line, end="")
    else:
        # print(f"Subbing {old} with {new}")
        new_line = re.sub(old, new, line, 1)
        print(new_line, end="")

def find_delimiter(string):
    # Find the index of 's' in the string. This assumes 's' is not present in the address regex ;-;
    s_index = string.find('s')
    if s_index != -1 and s_index < len(string) - 1:
        # Extract the character following 's'
        delimiter = string[s_index + 1]

        #Consider cases of special chars
        if (delimiter == '?'):
            return r'\?'

        return delimiter
    else:
        return None
    
def get_subst_command_opts(arg):
    # print(arg)
    delimiter = find_delimiter(arg)
    # print(delimiter)
    
    trimmed_opts = re.split(delimiter, arg)
    # trimmed_opts = re.split('?', arg)
    # print("Trimmed options: ", *trimmed_opts)
    if (trimmed_opts[0] == ""):
        trimmed_opts = trimmed_opts[1:]
    re_addr = ""
    num_addr = [-1]
    glob = False
    new = trimmed_opts[len(trimmed_opts) - 2]
    old = trimmed_opts[len(trimmed_opts) - 3]
    
    # print("OLD: ", old)
    # for count, opt in enumerate(trimmed_opts):
    #     print(f"Opt {count}: {opt}")

    # print(*trimmed_opts)
    #If first arg is in form Ns
    if ('s' in trimmed_opts[0]):
        #If num_addr given, set
        if (trimmed_opts[0] != 's'):
            # print(trimmed_opts[0])
            num_addr = [int(trimmed_opts[0][0])]
    #If first arg is a regex, set
    else:
        re_addr = trimmed_opts[0]
    
    #If last arg is g - set global 
    if (trimmed_opts[len(trimmed_opts) - 1] == 'g'):
        glob = True

    return re_addr, num_addr, glob, old, new

        
              



def main():
    n_flag, command_args = get_commands()
    # print(*command_args)
    for command_arg in command_args:
        command, line_num, pattern = parse_command(command_arg)
        # print(f"Command: {command}, Relevant line(s): {line_num}, Pattern: {pattern}")
        match command:
            case "quit":
                quit(line_num, pattern)
            case "print":
                if (n_flag):
                    print_n(line_num, pattern)
                else:
                    print_ln(line_num, pattern)
            case "delete":
                if (n_flag):
                    pass
                else:
                    delete(line_num, pattern)
            case "subst":
                re_addr, num_addr, glob, old, new = get_subst_command_opts(command_arg)
                # print(f"regex_addr: {re_addr}, line_addr: {num_addr}, isGlobal: {glob}, old: {old}, new: {new}")
                substitute(re_addr, num_addr, old, new, glob)

if __name__ == '__main__':
    main()

