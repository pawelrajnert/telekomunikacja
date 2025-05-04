from queue import PriorityQueue


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


def prepareTree(text):
    def countLetters(txt):
        tmp = list(txt)
        tmp.sort()
        txt = ''.join(tmp)
        tmp.clear()
        pom = 0
        result = {}
        for i in range(0, len(txt)):
            pom += 1
            if i == len(txt) - 1:
                result[txt[i]] = pom
            elif txt[i] != txt[i + 1]:
                result[txt[i]] = pom
                pom = 0
        return result

    nodes = PriorityQueue()
    letters = countLetters(text)
    for l in letters:
        node = Node(letters[l], l)
        nodes.put(node)
    root = None
    while nodes.qsize() > 1:
        first = nodes.get()
        second = nodes.get()
        if first.value == second.value and not first.isContainingLetter():
            first, second = second, first
        head = Node(first.value + second.value, "")
        root = head
        head.leftChild = first
        head.rightChild = second
        nodes.put(head)
    return root, letters
