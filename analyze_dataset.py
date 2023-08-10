import os
import glob
from skimage import io
import csv
import extcolors
from colormap import rgb2hex


# in the data frame, import the images
dataset_picture_path = 'images'
artist_names = ['Alfred_Sisley', 'Amedeo_Modigliani', 'Andrei_Rublev', 'Andy_Warhol', 'Camille_Pissarro', 'Caravaggio',
                'Claude_Monet', 'Diego_Rivera', 'Edgar_Degas', 'Edouard_Manet', 'Edvard_Munch',
                'El_Greco', 'Eugene_Delacroix', 'Francisco_Goya', 'Frida_Kahlo', 'Georges_Seurat', 'Giotto_di_Bondone',
                'Gustav_Klimt', 'Gustave_Courbet', 'Henri_de_Toulouse-Lautrec', 'Henri_Matisse', 'Henri_Rousseau',
                'Hieronymus_Bosch', 'Jackson_Pollock', 'Jan_van_Eyck', 'Joan_Miro', 'Kazimir_Malevich',
                'Leonardo_da_Vinci', 'Marc_Chagall', 'Michelangelo', 'Mikhail_Vrubel', 'Pablo_Picasso', 'Paul_Cezanne',
                'Paul_Gauguin', 'Paul_Klee', 'Peter_Paul_Rubens', 'Pierre-Auguste_Renoir', 'Piet_Mondrian',
                'Pieter_Bruegel', 'Raphael', 'Rembrandt', 'Rene_Magritte', 'Salvador_Dali', 'Sandro_Botticelli',
                'Titian', 'Vasiliy_Kandinskiy', 'Vincent_van_Gogh', 'William_Turner']

def rgb_codes(colours):
    colour_list = str(colours).replace('([(', '').split(', (')[0:-1]
    rgb_values = [i.split('), ')[0] + ')' for i in colour_list]
    # print(colour_list)
    return rgb_values

def hex_codes(colours):
    rgb_code = rgb_codes(colours)
    hex_code = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                        int(i.split(", ")[1]),
                        int(i.split(", ")[2].replace(")", ""))) for i in rgb_code]
    return hex_code


def save_csv(hex_code, pic_code):
    colour_data = [pic_code]
    for v_hex in zip(hex_code):
        hex_value = v_hex[0].replace("(", "").replace(")", "").replace("'", "")
        colour_data.append(hex_value)
    with open('Data\colour_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        field = [""]
        writer.writerow(colour_data)



categories = ['painting_code', 'colour #1', 'colour #2', 'colour #3', 'colour #4', 'colour #5']
with open('Data\colour_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(categories)

for artist in artist_names:
    paintings_paths = glob.glob(os.path.join(dataset_picture_path, artist, '*'))
    for painting_path in paintings_paths:

        painting_name = os.path.basename(painting_path)
        painting_pic = io.imread(painting_path)
        colours_extracted = extcolors.extract_from_path(painting_path, tolerance=20 , limit=6)
        colours = hex_codes(colours_extracted)
        if len(colours) == 5:
            save_csv(hex_codes(colours_extracted), painting_name)
            print(f"painting {painting_name} saved.")