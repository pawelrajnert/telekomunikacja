from queue import PriorityQueue
from Nodes import Node

def countLetters(text):
    tmp = list(text)
    tmp.sort()
    text = ''.join(tmp)
    tmp.clear()
    pom = 0
    result = {}
    for i in range(0, len(text)):
        pom += 1
        if i == len(text) - 1:
            result[text[i]] = pom
        elif text[i] != text[i + 1]:
            result[text[i]] = pom
            pom = 0
    return result

def prepareTree(text):
    letterOccurrences = countLetters(text)
    nodes = PriorityQueue()
    for l in letterOccurrences:
        node = Node(letterOccurrences[l], l)
        nodes.put(node)
    while not nodes.empty():
        element = nodes.get()
        print(element.letter)

while True:
    print("1 - Wprowadź tekst do zakodowania")
    print("2 - Zakoduj plik tekstowy")
    print("3 - Prześlij plik")
    print("4 - Odbierz plik")
    print("Inna opcja - zakończ program")
    wybor = input("Wybor: ")
    if wybor == "1":
        tekst = input("Wpisz tekst do zakodowania: ")
        prepareTree(tekst)
    elif wybor == "2":
        print("2")
    elif wybor == "3":
        print("3")
    elif wybor == "4":
        print("4")
    else:
        break;
    input("Wciśnij enter by kontynuować")
