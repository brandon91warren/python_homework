# Task 1
def hello():
    return "Hello"

print(hello())

# Task 2
def greet(name):
    return f"Hello, {name}!"

print("Task 2:", greet("Brandon"))


# Task 3
def calc(a, b, op="multiply"):
    try:
        match op:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b
            case "modulo":
                return a % b
            case "int_divide":
                return a // b
            case "power":
                return a ** b
            case _:
                return None
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"

print("Task 3 add:", calc(5, 3, "add"))
print("Task 3 divide by zero:", calc(10, 0, "divide"))
print("Task 3 invalid multiply:", calc("a", "b"))

# Task 4
def data_type_conversion(value, type_name):
    try:
        match type_name:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
            case _:
                return None
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {type_name}."

print("Task 4 int:", data_type_conversion("12", "int"))
print("Task 4 bad float:", data_type_conversion("abc", "float"))


# Task 5
def grade(*args):
    try:
        avg = sum(args) / len(args)
    except Exception:
        return "Invalid data was provided."

    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

print("Task 5 grade:", grade(90, 80, 100))
print("Task 5 invalid:", grade("a", 5))

# Task 6
def repeat(string, count):
    result = ""
    for _ in range(count):
        result += string
    return result

print("Task 6:", repeat("ha", 3))

# Task 7
def student_scores(mode, **kwargs):
    if mode == "best":
        # highest score → return student name
        return max(kwargs, key=lambda name: kwargs[name])
    elif mode == "mean":
        # average score
        return sum(kwargs.values()) / len(kwargs)
    else:
        return None

print("Task 7 best:", student_scores("best", alice=88, bob=95, carol=82))
print("Task 7 mean:", student_scores("mean", alice=90, bob=80, carol=100))

# Task 8
def titleize(text):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}

    words = text.split()

    result_words = []

    for i, word in enumerate(words):
        # Always capitalize first and last
        if i == 0 or i == len(words) - 1:
            result_words.append(word.capitalize())
        elif word in little_words:
            result_words.append(word.lower())
        else:
            result_words.append(word.capitalize())

    return " ".join(result_words)

print("Task 8:", titleize("the lord of the rings"))

# Task 9
def hangman(secret, guess):
    result = ""

    for char in secret:
        if char in guess:
            result += char
        else:
            result += "_"

    return result

print("Task 9:", hangman("alphabet", "ab"))

# Task 10
def pig_latin(text):
    vowels = "aeiou"
    words = text.split()
    result = []

    for word in words:
        # Rule 3: special case for "qu"
        if word.startswith("qu"):
            result.append(word[2:] + "quay")
        # Rule 1: starts with vowel
        elif word[0] in vowels:
            result.append(word + "ay")
        # Rule 2: starts with consonant(s)
        else:
            # find first vowel
            i = 0
            while i < len(word) and word[i] not in vowels:
                i += 1
            result.append(word[i:] + word[:i] + "ay")

    return " ".join(result)

print("Task 10:", pig_latin("quick brown fox jumps over the lazy dog"))
