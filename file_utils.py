
def _blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def get_line_count(file_name):
    with open(file_name, "r", encoding="utf-8" ) as f:
        line_count = sum(bl.count("\n") for bl in _blocks(f))
    return line_count

def clear_file(file_name):
    open(file_name, 'w').close()
