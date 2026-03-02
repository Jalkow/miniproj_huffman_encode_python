"""
NodeHuffman class to build and manage nodes in huffman rooted tree
"""
class NodeHuffman :
  """
  Node class that represent nodes in huffman rooted tree
  
  A node is composed of:
    - A character
    - A frequency
    - A left children
    - A right children
  """

  def __init__(self, frequency, character="", left_child=None, right_child=None):
    self.character = character
    self.frequency = frequency
    self.left_child = left_child
    self.right_child = right_child
  
  def get_character(self):
    """
      Return the character of the node
      get_character : Node -> String
    """
    return self.character

  def get_frequency(self):
    """
      Return the frequency of the node
      get_frequency : Node -> Int
    """
    return self.frequency
  
  def get_left_child(self):
    """
      Return the left child of the node
      get_left_child : Node -> Node
    """
    return self.left_child
  
  def get_right_child(self):
    """
      Return the right child of the node
      get__right_child : Node -> Node
    """
    return self.right_child