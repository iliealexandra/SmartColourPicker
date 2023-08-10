import os
import csv
import extcolors
from colormap import rgb2hex


def analyze_picture(picture_path,t):
    colours = extcolors.extract_from_path(picture_path, tolerance=t , limit=6)
    colour_list = str(colours).replace('([(', '').split(', (')[0:-1]
    rgb_values = [i.split('), ')[0] + ')' for i in colour_list]
    hex_code = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                        int(i.split(", ")[1]),
                        int(i.split(", ")[2].replace(")", ""))) for i in rgb_values]
    return hex_code


def save_data(colour_code, pic_name):
    with open('Data/search_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pic_name] + colour_code)


def process_picture(picture_path,t):
    picture_name = os.path.basename(picture_path)
    colour_code = analyze_picture(picture_path,t)
    save_data(colour_code, picture_name)



# picture_path = 'test_pictures/coast.png'
# process_picture(picture_path)
