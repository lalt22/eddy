def find_delimiter(string):
    # Find the index of 's' in the string
    s_index = string.find('s')
    if s_index != -1 and s_index < len(string) - 1:
        # Extract the character following 's'
        delimiter = string[s_index + 1]
        return delimiter
    else:
        return None

# Test cases
strings = [
    "s?[15]?zzz?",
    "s_[15]_zzz_",
    "sX[15]XzzzX",
    "sX[15]Xz/z/zX"
]

for string in strings:
    delimiter = find_delimiter(string)
    print(f"String: {string}, Delimiter: {delimiter}")
