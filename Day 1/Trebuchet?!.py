# Part One
def extract_two_digits_number(text: str) -> int:
    digits = list(filter(str.isdigit, text))
    first_digit = int(digits[0])
    second_digit = int(digits[len(digits) - 1]) if len(digits) > 1 else first_digit
    return int(f"{first_digit}{second_digit}")


assert extract_two_digits_number("1abc2") == 12
assert extract_two_digits_number("pqr3stu8vwx") == 38
assert extract_two_digits_number("a1b2c3d4e5f") == 15
assert extract_two_digits_number("treb7uchet") == 77

with open('Input 1.txt') as f:
    lines = f.readlines()
    sum = 0
    for line in lines:
        sum += extract_two_digits_number(line)
    print(sum)


# Part Two
def extract_two_digits_number_with_words(text: str) -> int:
    first_digit = ""
    last_digit = ""
    for index, char in enumerate(text):
        digit = char if char.isdigit() else ""
        digit = 1 if text[index:index + 3] == "one" else digit
        digit = 2 if text[index:index + 3] == "two" else digit
        digit = 3 if text[index:index + 5] == "three" else digit
        digit = 4 if text[index:index + 4] == "four" else digit
        digit = 5 if text[index:index + 4] == "five" else digit
        digit = 6 if text[index:index + 3] == "six" else digit
        digit = 7 if text[index:index + 5] == "seven" else digit
        digit = 8 if text[index:index + 5] == "eight" else digit
        digit = 9 if text[index:index + 4] == "nine" else digit
        if digit != "":
            if first_digit == "":
                first_digit = digit
            last_digit = digit
    return int(f"{first_digit}{last_digit}")


assert extract_two_digits_number_with_words("two1nine") == 29
assert extract_two_digits_number_with_words("eightwothree") == 83
assert extract_two_digits_number_with_words("abcone2threexyz") == 13
assert extract_two_digits_number_with_words("xtwone3four") == 24
assert extract_two_digits_number_with_words("4nineeightseven2") == 42
assert extract_two_digits_number_with_words("zoneight234") == 14
assert extract_two_digits_number_with_words("7pqrstsixteen") == 76

with open('Input 2.txt') as f:
    lines = f.readlines()
    sum = 0
    for line in lines:
        sum += extract_two_digits_number_with_words(line)
    print(sum)
