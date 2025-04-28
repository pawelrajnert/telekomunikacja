class Node:
    value = 0
    letter = ""
    rightChild = None
    leftChild = None

    def __init__(self, v, l):
        self.value = v
        self.letter = l

    def isContainingLetter(self):
        return self.letter != ""

    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        if not self.isContainingLetter() and other.isContainingLetter():
            return True
        if self.isContainingLetter() and not other.isContainingLetter():
            return False
        if self.isContainingLetter() and other.isContainingLetter():
            return ord(self.letter) < ord(other.letter)
        return True
