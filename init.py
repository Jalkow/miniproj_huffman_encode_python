import os
from HuffmanTextEncoder import *

working_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(working_dir, "donnees")
output_folder = os.path.join(working_dir, "outputs/")

for filename in os.listdir(data_folder):
    path_to_file = os.path.join(data_folder, filename)

    # Recuperation texte dans le fichier
    with open(path_to_file, "r", encoding="utf-8") as file:
        text_to_encode = file.read()

    # Préparation de l'encoder (generation frequence par carac et arbre de Huffman)
    encoder = HuffmanTextEncoder(text_to_encode)
    
    # Encodage du texte (generation fichier bin et frequence)
    encoder.encode_text(os.path.splitext(filename)[0], output_folder)