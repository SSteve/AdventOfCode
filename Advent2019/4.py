# pw is a list of single-digit integers representing the six digits of the password
def valid_password1(pw):
    found_equal_adjacent = False
    for i in range(1, len(pw)):
        if pw[i] < pw[i - 1]:
            return False
        if pw[i] == pw[i - 1]:
            found_equal_adjacent = True
    return found_equal_adjacent
    
def valid_password2(pw):
    fewest_repeats_in_group = len(pw)
    repeats_in_group = 0
    found_equal_adjacent = False
    for i in range(1, len(pw)):
        if pw[i] < pw[i - 1]:
            return False
        if pw[i] == pw[i - 1]:
            if not found_equal_adjacent:
                repeats_in_group = 2
            else:
                repeats_in_group += 1
            found_equal_adjacent = True
        elif found_equal_adjacent:
            fewest_repeats_in_group = min(fewest_repeats_in_group, repeats_in_group)
            found_equal_adjacent = False
    # We were in a group at the end of the password. If it's a group of 2, this is a valid password
    if found_equal_adjacent and repeats_in_group == 2:
        return True
    return fewest_repeats_in_group == 2
    
# pw is an integer
def password_to_list(pw, number_of_digits):
    the_list = []
    for _ in range(number_of_digits):
        the_list.insert(0, pw % 10)
        pw //= 10
    return the_list
    
# pw_list is a list of single-digit integers
def list_to_value(pw_list):
    the_value = 0
    for digit in pw_list:
        the_value = the_value * 10 + digit
    return the_value

def count_passwords(start, end, method = 1):
    valid_password = valid_password1 if method == 1 else valid_password2
    valid_passwords = 0
    start_pw = password_to_list(start, 6)
    try:
        for digit1 in range(start // 100_000, 10):
            for digit2 in range(digit1, 10):
                for digit3 in range(digit2, 10):
                    for digit4 in range(digit3, 10):
                        for digit5 in range(digit4, 10):
                            for digit6 in range(digit5, 10):
                                pw_list = [digit1, digit2, digit3, digit4, digit5, digit6]
                                pw_value = list_to_value(pw_list)
                                if pw_value < start:
                                    continue
                                if pw_value > end:
                                    raise ValueError
                                
                                if valid_password(pw_list):
                                    valid_passwords += 1
    except ValueError:
        pass

    return valid_passwords

if __name__ == "__main__":
    # Tests
    assert valid_password1(password_to_list(111111, 6)), "Test 1 failed"
    assert not valid_password1(password_to_list(223450, 6)), "Test 2 failed"
    assert not valid_password1(password_to_list(123789, 6)), "Test 3 failed"
    assert valid_password2(password_to_list(112233, 6)), "Test 4 failed"
    assert not valid_password2(password_to_list(123444, 6)), "Test 5 failed"
    assert valid_password2(password_to_list(111122, 6)), "Test 6 failed"
    
    print(f"Part one: {count_passwords(246515, 739105)} valid passwords.")
    print(f"Part two: {count_passwords(246515, 739105, 2)} valid passwords.")