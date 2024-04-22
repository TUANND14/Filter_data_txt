import re

def find_text_block(file_path, string):
    # tung
    # thang
    result = ""
    text_block = ""
    string_list = string.split()
    for charecter in string_list:
        word = rf"\b{charecter.strip()}\b"
        is_in_block = False
        with open(file_path, 'r') as f:
            for line in f:
                # if string in line:
                if re.search(word, line):
                    is_in_block = True
                    text_block += line
                elif is_in_block:
                    if not line.strip():
                        result+= text_block
                        text_block = ""
                        is_in_block = False
                    text_block += line
                else:
                    if not line.strip():
                        text_block = ""
                    text_block +=line
                    is_in_block = False
        if is_in_block:
            result+= text_block

    return result
# ham them vao nham chia tach du lieu
def split_text (a):
    return a.split("\n")
file_path = "data.txt"
string = " tung\n       thang   "
print(find_text_block(file_path, string))

