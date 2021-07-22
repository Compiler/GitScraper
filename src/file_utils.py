
def _blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def get_line_count(file_name):
    with open(file_name, "r+", encoding="utf-8") as f:
        line_count = sum(bl.count("\n") for bl in _blocks(f))
    return line_count

def clear_file(file_name):
    open(file_name, 'w').close()

def add_newline_if_missing(filename):
    with open(filename, 'r+', encoding='utf-8') as input_file:
        if(input_file.read()[-1] != '\n'):
            input_file.write("\n")
            input_file.close()

def get_last_line(filename):
    with open(filename, 'r') as f:
        return f.readlines()[-1]
