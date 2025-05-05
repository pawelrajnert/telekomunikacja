def encodeLetters(letters, node, code):
    if node is None:
        return letters
    if node.isContainingLetter():
        letters[node.letter] = code
    encodeLetters(letters, node.leftChild, code + "0")
    encodeLetters(letters, node.rightChild, code + "1")
    return letters


def encodeText(text, code):
    result = ""
    for letter in text:
        result += code[letter]
    return result


def decodeText(encodedText, code):
    reversedCode = {}
    for key, value in code.items():
        reversedCode[value] = key
    result = ""
    bits = ""
    for bit in encodedText:
        bits += bit
        if bits in reversedCode:
            result += reversedCode[bits]
            bits = ""
    return result
