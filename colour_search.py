import math
import csv

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return r, g, b

def rgb_to_xyz(rgb):
    r, g, b = [x / 255 for x in rgb]

    r = gamma_correction(r)
    g = gamma_correction(g)
    b = gamma_correction(b)

    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b

    return x, y, z

def gamma_correction(color):
    if color <= 0.04045:
        return color / 12.92
    else:
        return ((color + 0.055) / 1.055) ** 2.4

def xyz_to_lab(xyz):
    x, y, z = xyz

    x = x / 0.95047
    y = y / 1.00000
    z = z / 1.08883

    fx = f(x)
    fy = f(y)
    fz = f(z)

    l = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)

    return l, a, b

def f(t):
    if t > 0.008856:
        return t ** (1/3)
    else:
        return (903.3 * t) + 16 / 116

def hex_to_lab(hex_value):
    rgb_values = hex_to_rgb(hex_value)
    xyz_values = rgb_to_xyz(rgb_values)
    lab_values = xyz_to_lab(xyz_values)
    return lab_values

def ciede2000(lab1, lab2):


    l1, a1, b1 = lab1
    l2, a2, b2 = lab2


    c1 = math.sqrt(a1 ** 2 + b1 ** 2)
    c2 = math.sqrt(a2 ** 2 + b2 ** 2)
    c_bar = (c1 + c2) / 2

    g = 0.5 * (1 - math.sqrt(c_bar ** 7 / (c_bar ** 7 + 25 ** 7)))

    a1_p = (1 + g) * a1
    a2_p = (1 + g) * a2

    c1_p = math.sqrt(a1_p ** 2 + b1 ** 2)
    c2_p = math.sqrt(a2_p ** 2 + b2 ** 2)

    h1_p = math.atan2(b1, a1_p)
    h1_p = math.degrees(h1_p)
    if h1_p < 0:
        h1_p += 360

    h2_p = math.atan2(b2, a2_p)
    h2_p = math.degrees(h2_p)
    if h2_p < 0:
        h2_p += 360

    delta_l_p = l2 - l1
    delta_c_p = c2_p - c1_p

    h_delta_p = h2_p - h1_p
    if abs(h_delta_p) > 180:
        if h2_p <= h1_p:
            h_delta_p += 360
        else:
            h_delta_p -= 360

    delta_h_p = 2 * math.sqrt(c1_p * c2_p) * math.sin(math.radians(h_delta_p) / 2)

    l_avg = (l1 + l2) / 2
    c_avg_p = (c1_p + c2_p) / 2

    h_avg_p = (h1_p + h2_p) / 2
    if abs(h1_p - h2_p) > 180:
        h_avg_p += 180

    t = 1 - 0.17 * math.cos(math.radians(h_avg_p - 30)) + 0.24 * math.cos(math.radians(2 * h_avg_p)) + 0.32 * math.cos(math.radians(3 * h_avg_p + 6)) - 0.20 * math.cos(math.radians(4 * h_avg_p - 63))

    delta_theta = 30 * math.exp(-((h_avg_p - 275) / 25) ** 2)
    r_c = 2 * math.sqrt(c_avg_p ** 7 / (c_avg_p ** 7 + 25 ** 7))
    s_l = 1 + (0.015 * (l_avg - 50) ** 2) / math.sqrt(20 + (l_avg - 50) ** 2)
    s_c = 1 + 0.045 * c_avg_p
    s_h = 1 + 0.015 * c_avg_p * t

    delta_ro = 30 * math.exp(-((h_avg_p - 275) / 25) ** 2) * r_c * s_h

    c_avg_p7 = c_avg_p ** 7
    r_t = -math.sin(2 * math.radians(delta_theta)) * delta_ro

    delta_e = math.sqrt(max(0, (delta_l_p / (s_l)) ** 2 + (delta_c_p / (s_c)) ** 2 + (delta_h_p / (s_h)) ** 2 + (delta_ro / (s_c)) * (delta_ro / (s_c)) * r_t))
    return delta_e


def color_palette_difference(palette1, palette2):
    lab_palette1 = []
    for hex_code in palette1:
        rgb_values = hex_to_rgb(hex_code)
        xyz_values = rgb_to_xyz(rgb_values)
        lab_values = xyz_to_lab(xyz_values)
        lab_palette1.append(lab_values)

    lab_palette2 = []
    for hex_code in palette2:
        rgb_values = hex_to_rgb(hex_code)
        xyz_values = rgb_to_xyz(rgb_values)
        lab_values = xyz_to_lab(xyz_values)
        lab_palette2.append(lab_values)

    differences=[]

    for colour1 in palette1:
        min_difference = float('inf')
        for colour2 in palette2:
            lab1 = hex_to_lab(colour1)
            lab2 = hex_to_lab(colour2)
            difference = ciede2000(lab1, lab2)
            if difference < min_difference:
                min_difference = difference
        differences.append(min_difference)
    average_difference = sum(differences) / len(differences)

    return average_difference


def read_last_row_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        rows = list(reader)
        last_row = rows[-1]
    return last_row[1:]  # Exclude the 'search' column


def read_color_palette_from_csv(file_path):
    palette = []
    painting_codes = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            painting_codes.append(row[0])
            palette.append(row[1:])
    return painting_codes, palette

def find_closest_paintings(user_palette, painting_codes, palette, top_n=8):
    differences = []
    closest_paintings = []

    for i in range(len(palette)):
        difference = color_palette_difference(user_palette, palette[i])
        differences.append(difference)
        closest_paintings.append(painting_codes[i])

    top_smallest_differences = sorted(range(len(differences)), key=lambda i: differences[i])[:top_n]
    top_closest_paintings = [closest_paintings[i] for i in top_smallest_differences]
    top_differences = [differences[i] for i in top_smallest_differences]

    return top_closest_paintings, top_differences


def colour_search_results():
    user_palette = read_last_row_from_csv('Data/search_data.csv')
    painting_codes, palette = read_color_palette_from_csv('Data/colour_data.csv')
    top_paintings, top_differences = find_closest_paintings(user_palette, painting_codes, palette, top_n=8)

    # Create a list of dictionaries for the top results
    top_results = []
    for i in range(len(top_paintings)):
        painting_code = top_paintings[i]
        painting_index = painting_codes.index(painting_code)
        colours = palette[painting_index]

        result = {
            'Painting Code': painting_code,
            'Colour #1': colours[0],
            'Colour #2': colours[1],
            'Colour #3': colours[2],
            'Colour #4': colours[3],
            'Colour #5': colours[4]
        }
        top_results.append(result)

    # Save the top results to the CSV file
    file_path = 'Data/search_results.csv'
    fieldnames = ['Painting Code', 'Colour #1', 'Colour #2', 'Colour #3', 'Colour #4', 'Colour #5']
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top_results)



