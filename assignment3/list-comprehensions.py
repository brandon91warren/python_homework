import csv

data = []
with open("../csv/employees.csv", newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

rows = data[1:]

full_names = [f"{row[1]} {row[2]}" for row in rows]
print(full_names)

names_with_e = [name for name in full_names if "e" in name.lower()]
print(names_with_e)
