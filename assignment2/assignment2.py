import csv
import traceback
import os
from datetime import datetime
import custom_module

def format_exception(e):
    import traceback
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = [
        f'File: {t[0]}, Line: {t[1]}, Func: {t[2]}, Msg: {t[3]}'
        for t in trace_back
    ]
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")

def read_employees():
    data = {}
    rows = []
    try:
        with open("../csv/employees.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    data["fields"] = row
                else:
                    rows.append(row)
        data["rows"] = rows
        return data
    except Exception as e:
        format_exception(e)
        raise

employees = read_employees()

def column_index(column_name):
    try:
        return employees["fields"].index(column_name)
    except Exception as e:
        format_exception(e)
        raise

employee_id_column = column_index("employee_id")

def first_name(row_number):
    try:
        idx = column_index("first_name")
        row = employees["rows"][row_number]
        return row[idx]
    except Exception as e:
        format_exception(e)
        raise

def employee_find(employee_id):
    try:
        def employee_match(row):
            return int(row[employee_id_column]) == employee_id
        matches = list(filter(employee_match, employees["rows"]))
        return matches
    except Exception as e:
        format_exception(e)
        raise

def employee_find_2(employee_id):
    try:
        matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
        return matches
    except Exception as e:
        format_exception(e)
        raise

def sort_by_last_name():
    try:
        idx = column_index("last_name")
        employees["rows"].sort(key=lambda row: row[idx])
        return employees["rows"]
    except Exception as e:
        format_exception(e)
        raise

def employee_dict(row):
    try:
        idx_id = column_index("employee_id")
        fields = [f for i, f in enumerate(employees["fields"]) if i != idx_id]
        values = [v for i, v in enumerate(row) if i != idx_id]
        return dict(zip(fields, values))
    except Exception as e:
        format_exception(e)
        raise

def all_employees_dict():
    try:
        result = {}
        for row in employees["rows"]:
            emp_id = row[employee_id_column]
            result[emp_id] = employee_dict(row)
        return result
    except Exception as e:
        format_exception(e)
        raise

def get_this_value():
    try:
        return os.getenv("THISVALUE")
    except Exception as e:
        format_exception(e)
        raise

def set_that_secret(new_value):
    try:
        custom_module.set_secret(new_value)
    except Exception as e:
        format_exception(e)
        raise

def read_csv_as_dict(file_path):
    try:
        data = {}
        rows = []
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if idx == 0:
                    data["fields"] = row
                else:
                    rows.append(tuple(row))
        data["rows"] = rows
        return data
    except Exception as e:
        format_exception(e)
        raise

def read_minutes():
    minutes1 = read_csv_as_dict("../csv/minutes1.csv")
    minutes2 = read_csv_as_dict("../csv/minutes2.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()

def create_minutes_set():
    try:
        set1 = set(minutes1["rows"])
        set2 = set(minutes2["rows"])
        return set1.union(set2)
    except Exception as e:
        format_exception(e)
        raise

minutes_set = create_minutes_set()

def create_minutes_list():
    try:
        lst = list(minutes_set)
        result = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), lst))
        return result
    except Exception as e:
        format_exception(e)
        raise

minutes_list = create_minutes_list()

def write_sorted_list():
    try:
        minutes_list.sort(key=lambda x: x[1])
        out_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), minutes_list))
        with open("minutes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(minutes1["fields"])
            writer.writerows(out_list)
        return out_list
    except Exception as e:
        format_exception(e)
        raise
