

def validate_input(input):
    if input is not None and (len(input) > 50 or any(char.isdigit() for char in input)):
        return False
    return True
