def count_percentage(letter, string):
    count = 0
    total_letters = sum(1 for char in string if char.isalpha())
    for char in string:
        if char == letter:
            count += 1
    percentage = (count / total_letters) * 100
    return percentage

# Example usage
string = "!@#Hello World!^"
letter = "l"
percentage = count_percentage(letter, string)
print(f"The letter '{letter}' appears in the string '{string}' {percentage:.2f}% of the time.")