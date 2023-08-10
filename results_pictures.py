import csv
import re
import os


def get_folder(strings):
    result = []
    for string in strings:
        match = re.search(r'_(\d+)$', string)
        if match:
            string_without_number = re.sub(r'_(\d+)$', '', string)
            result.append(string_without_number)
    return result


def read_column_values(filename, column_index):
    column_values = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            column_values.append(row[column_index])
    return column_values


def remove_extension(strings, extension):
    return [string.replace(extension, '') for string in strings]


def create_path(filename):
    column_index = 0
    column_values = read_column_values(filename, column_index)
    pic_codes = remove_extension(column_values, '.jpg')
    cleaned_values = get_folder(pic_codes)

    dir_path = 'images'
    paths = []
    for subdir, column_value in zip(cleaned_values, column_values):
        path = os.path.join(dir_path, subdir, column_value)
        paths.append(path)

    return paths
