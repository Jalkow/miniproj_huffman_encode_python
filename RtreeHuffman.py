# -*- coding: utf-8 -*-
from NodeHuffman import NodeHuffman
from collections import deque
"""
RTreeHuffman module to build and manage Huffman rooted tree, that allows to assign a binary code to characters based on it's frequency 
(the more frequent the character the less bits it will need)
"""
class RtreeHuffman:
  
  """
  Build a rooted huffman tree by giving it the dictionnary of characters and their frequency
  Or by giving it it's root
  """
  def __init__(self, root=None, dict_frequency_per_char=None):
    if root is not None:
      self.root = root

    elif dict_frequency_per_char is not None:
      forest = [] # List des sub-trees (représentés par les nodes root) à mettre dans l'arbre de Huffman
      for character, frequency in dict_frequency_per_char.items():
          forest.append(NodeHuffman(frequency, character))
    
      while(len(forest) > 1): # S'arrête quand il n'y a plus que 1 element (qui est le root de l'arbre de Huffman complété)
        forest.sort(key=lambda node: node.frequency) # Sort pour pouvoir pop les deux premiers elements qui sont les nodes avec les plus petites fréquences

        t1 = forest.pop(0) # node avec la plus basse frequence
        t2 = forest.pop(0) # node avec la 2ème plus basse frequence

        # Création nouveau node qui a ces deux nodes comme enfants (à gauche node plus petite frequence)
        new_tree_root = NodeHuffman(t1.get_frequency() + t2.get_frequency(), left_child=t1, right_child=t2)

        forest.append(new_tree_root)
      
      
      self.root = forest[0]


  def get_root(self):
    """
      Return the root of the rooted tree
      get_root : RtreeHuffman -> NodeHuffman
    """
    return self.root


  def get_characters_bit_representations(self, actual_bit_value="", actual_bit_representations={}):
    """
      Returns a dict with the characters as the keys and their bit representation as the values by traversing the huffman tree
      get_characters_bit_representations : RtreeHuffman -> Dict
    """

    # Quant on arrive sur un node qui a un character on met la val en bit qu'on a actuellement dans le dict à la clé du character
    if(self.root.get_character() != ""):
       actual_bit_representations[self.root.get_character()] = actual_bit_value

    if(self.root.get_left_child() is not None):
       RtreeHuffman(root=self.root.get_left_child()).get_characters_bit_representations(actual_bit_value + "0", actual_bit_representations)

    if(self.root.get_right_child() is not None):
       RtreeHuffman(root=self.root.get_right_child()).get_characters_bit_representations(actual_bit_value + "1", actual_bit_representations)

    return actual_bit_representations


