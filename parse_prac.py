import re 
import sys

SUBSTITUTION_PATTERN = r'\A(/[^/]*/){0,1}\d*s\S(\[*[^\]/]*\]*)\S[\w\-/]*\Sg{0,1}'
QUIT_PATTERN = r'.*q\Z'
DELETE_PATTERN = r'.*d\Z'
NUM_ADDR_PATTERN = r'\A\d+\Z'
REGEX_ADDR_PATTERN = r'\A\S+\Z'

def parse_command(string):
    if (re.match(QUIT_PATTERN, string)):
        address = string.split('q')
        print(address)
        if (re.match(NUM_ADDR_PATTERN, address[0])):
            print("This is a num address")
        elif (re.match(REGEX_ADDR_PATTERN, address[0])):
            print("This is a regex address")
        else:
            print("No address given")
    elif (re.match(DELETE_PATTERN, string)):
        print("String is delete command")
    elif (re.match(SUBSTITUTION_PATTERN, string)):
        print("String is subst command")

def main():
    for arg in sys.argv[1:]:
        parse_command(arg)

if __name__ == '__main__':
    main()
