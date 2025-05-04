from mainMethods import *

inputText = ""
letterCodes = {}
encodedText = ""
decodedText = ""

while True:
    print("0 - wyczyść zmienne")
    print("1 - Wprowadź tekst do zakodowania")
    print("2 - Wprowadź tekst z plik tekstowego do zakodowania")
    print("3 - Utwórz słownik kodów dla wprowadzonych danych wejściowych i zakoduj tekst")
    print("4 - Odkoduj dane")
    print("5 - Porównaj odkodowany tekst z wprowadzonym")
    print("6 - Zapisz zakodowany tekst do pliku")
    print("7 - Wczytaj zakodowany tekst z pliku wraz ze słownikiem do odkodowania")
    print("8 - Nadaj wiadomość")
    print("9 - Odbierz wiadomość")
    print("Inna opcja - zakończ program")
    choice = input("Wybor: ")
    if choice == "0":
        inputText, letterCodes, encodedText, decodedText = "", {}, "", ""
    elif choice == "1":
        inputText = input("Wpisz tekst do zakodowania: ")
    elif choice == "2":
        inputText = readTextFile()
    elif choice == "3":
        letterCodes, encodedText = encodeData(inputText)
    elif choice == "4":
        decodedText = decodeData(letterCodes, encodedText)
    elif choice == "5":
        compareTexts(inputText, decodedText)
    elif choice == "6":
        saveData(letterCodes, encodedText)
    elif choice == "7":
        letterCodes, encodedText = readData()
    elif choice == "8":
        print("TODO")
    elif choice == "9":
        print("TODO")
    else:
        break
    input("Aby kontynuować, naciśnij enter...")
