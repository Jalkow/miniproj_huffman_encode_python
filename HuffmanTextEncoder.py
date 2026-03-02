from RtreeHuffman import RtreeHuffman

class HuffmanTextEncoder:
  def __init__(self, text):
    self.text = text
    self.dict_frequency_per_char_alphabet = {}
    self.huffman_tree = None
    self.encoded_bits_characters_dict = {}
    self.encoded_text_bytes = None

  """
    Encode the text that was given in the constructor, generating the encoded text as a binary file and
    an additionnal file with the number of characters in the alphabet and their frequencies in a text file
    this text file can later be used to decode the binary file
  """
  def encode_text(self, filename, output_dir):

    ### Obtention texte encodé sous forme de bits ###
    encoded_text_bits = ""
    self.generate_infos_needed_for_encoding()
    for char in self.text:
      encoded_text_bits += self.encoded_bits_characters_dict[char]
    
    ### Obtention du texte séparé par octets ###

    # Gérer le fait que le dernier octet peut ne pas être complet et donc que il va être complété par des 0
    numb_of_bits_missing_in_last_byte = 8 - (len(encoded_text_bits) % 8)
    if(numb_of_bits_missing_in_last_byte != 8):
      encoded_text_bits = encoded_text_bits + ("0" * numb_of_bits_missing_in_last_byte)

    # Séparation des bits par octets
    encoded_text_bytes = bytearray()
    for i in range(0, len(encoded_text_bits), 8):
      byte = encoded_text_bits[i:i+8]
      encoded_text_bytes.append(int(byte, 2))

    # Ajout d'un dernier octet qui stocke le nombre de 0 qu'on a ajouté pour compléter le dernier octet afin de pouvoir les enlever quand on décode
    encoded_text_bytes.append(numb_of_bits_missing_in_last_byte)

    # Affichage du taux de compression
    self.show_compression_rate(encoded_text_bytes, filename)

    # Création fichier encode bin et fichier de frequence
    self.create_encoded_file(filename, encoded_text_bytes, output_dir)
    self.create_frequency_file(filename, output_dir)

    return encoded_text_bits
  
  """
    Create a binary file containing the encoded text in bytes 
    and at the end of the file the number of 0 that was added in the last incomplete byte
  """
  def create_encoded_file(self, filename, encoded_text_bytes, output_dir):
    # wb pour write binary -> ecrire en binaire (si fichier existe pas ça le crée et si il existe déjà ça re-écrit ce que il y a dedans)
    with open(f"{output_dir}{filename}.bin", "wb") as file:
        file.write(encoded_text_bytes)

  """
    Create a text file containing the number of characters in the alphabet on the first line
    followed by every character of the alphabet and their frequency (ordered by ascending frequency and ASCII code)
  """
  def create_frequency_file(self, filename, output_dir):
    alphabet_size = len(self.dict_frequency_per_char_alphabet)

    with open(f"{output_dir}{filename}_freq.txt", "w", encoding="utf-8") as file:
      file.write(f"{alphabet_size}\n")
    
      for character, frequency in self.dict_frequency_per_char_alphabet.items():
          file.write(f"{character} {frequency}\n")

  """
    Generate informations required to encode the text 
    (dictionnary of alphabet with frequencies, Huffman tree and bit representation of characters of the alphabet)
  """
  def generate_infos_needed_for_encoding(self):
    new_dict_alphabet = self.determine_alphabet_with_frequencies()
    # Si dictionnaire a changé (ou qu'il n'y en avait pas avant) le texte a changé donc il faut regénérer l'arbre de Huffman
    if(new_dict_alphabet != self.dict_frequency_per_char_alphabet):
      self.dict_frequency_per_char_alphabet = new_dict_alphabet
      self.huffman_tree = RtreeHuffman(dict_frequency_per_char=self.dict_frequency_per_char_alphabet)
      self.encoded_bits_characters_dict = self.huffman_tree.get_characters_bit_representations()
  
  """
    Determines the frequency of appearance of every character of text to be encoded and save it in the 
    alphabet_dict_with_frequencies attribute in the form of a dict with the character as the key and the frequency as the value
  """
  def determine_alphabet_with_frequencies(self):
    alphabet_dict_with_frequencies = {}
    for char in self.text:
      if char in alphabet_dict_with_frequencies:
        alphabet_dict_with_frequencies[char] += 1
      else:
        alphabet_dict_with_frequencies[char] = 1

    # dict.items donne le couple (character, frequency) and le sorting est fait dans l'ordre du tuple donné dans lambda item (d'abord par fréquence puis valeur ASCII)
    return dict(sorted(alphabet_dict_with_frequencies.items(), key=lambda item: (item[1], item[0])))

  """
    Prints the compression rate of the encoded text (by comparing it's size in bytes)
  """
  def show_compression_rate(self, encoded_text_bytes, filename):
    nb_bytes_in_base_text = len(self.text)
    nb_bytes_in_encoded_text = len(encoded_text_bytes)

    print(f"Taux de compression du fichier {filename} : {1 - (nb_bytes_in_encoded_text / nb_bytes_in_base_text)}" )