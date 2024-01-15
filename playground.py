a = "asd"
b = None

c = ""

if a is not None:
    c += a

if b is not None:
    c += " " + b

if c is None or c == "":
    c = "John Doe"

print(c)