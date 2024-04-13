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


def get_subst_patterns(arg):
    strs = arg.split("/")
    return strs

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
    elif (chars[len(chars) - 1] == 'd'):
        if (chars[0] == "/"):
            pattern = arg[1:-2]
        else:
            if (len(chars) == 1):
                line_num = 0
            else:
                line_num = int(arg[0:-1])
        return "delete", line_num, pattern.strip()
    else:
        return "subst", -1, ""

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

def delete(line_num, pattern):
    for count, line in enumerate(sys.stdin):
        if (line_num == 0):
            break
        if (count == line_num - 1):
            continue
        elif (pattern != ""):
            if (re.search(pattern, line)):
                continue
        print(line, end="")

def substitute(re_addr, line_num, old, new, is_g):
    for count, line in enumerate(sys.stdin):
        #If only substutiting at num addr
        if (count == line_num - 1):
            get_and_sub_matches(line, old, new, is_g)
        #If only subbing at regexp addr
        elif (re_addr != ""):
            if (re.search(re_addr, line)):
                get_and_sub_matches(line, old, new, is_g)
            else:
                print(line, end="")
        #If subbing all lines that contain the old regex
        elif (line_num == -1):
            get_and_sub_matches(line, old, new, is_g)
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
    
def get_subst_command_opts(arg):
    trimmed_opts = arg.split("/")
    if (trimmed_opts[0] == ""):
        trimmed_opts = trimmed_opts[1:]
    re_addr = ""
    num_addr = -1
    glob = False
    new = trimmed_opts[len(trimmed_opts) - 2]
    old = trimmed_opts[len(trimmed_opts) - 3]
    

    # for count, opt in enumerate(trimmed_opts):
    #     print(f"Opt {count}: {opt}")

    # print(*trimmed_opts)
    #If first arg is in form Ns
    if ('s' in trimmed_opts[0]):
        #If num_addr given, set
        if (trimmed_opts[0] != 's'):
            # print(trimmed_opts[0])
            num_addr = int(trimmed_opts[0][0])
    #If first arg is a regex, set
    else:
        re_addr = trimmed_opts[0]
    
    #If last arg is g - set global 
    if (trimmed_opts[len(trimmed_opts) - 1] == 'g'):
        glob = True

    return re_addr, num_addr, glob, old, new

        
              



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

