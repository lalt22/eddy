import sys
import re

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
    pass

for arg in sys.argv[1:]:
    # print("Have arg: ", arg)
    command, line_num, pattern = parse_command(arg)
    match command:
        case "quit":
            # print("Line num: ", line_num)
            # print("Pattern: ", pattern)
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


