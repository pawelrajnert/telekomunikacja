from mainMethods import *

inputText = ""
letterCodes = {}
encodedText = ""
decodedText = ""

while True:
    print("Wybierz opcję: ")
    print("0 - Wyczyść zmienne")
    print("1 - Wprowadź tekst do zakodowania")
    print("2 - Wprowadź tekst z pliku tekstowego do zakodowania")
    print("3 - Utwórz słownik kodów dla wprowadzonych danych wejściowych i zakoduj tekst")
    print("4 - Odkoduj dane")
    print("5 - Porównaj odkodowany tekst z wprowadzonym")
    print("6 - Zapisz zakodowany tekst do pliku")
    print("7 - Wczytaj zakodowany tekst z pliku wraz ze słownikiem do odkodowania")
    print("8 - Zapisz odkodowany tekst do pliku")
    print("9 - Nadaj wiadomość na inny komputer")
    print("10 - Odbierz wiadomość z innego komputera")
    print("11 - Wypisz na ekran stan zmiennych programu")
    print("Inna opcja - zakończ program")
    choice = input("Wybór: ")
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
        saveText(decodedText)
    elif choice == "9":
        sendData(letterCodes, encodedText)
    elif choice == "10":
        letterCodes, encodedText = receiveData()
    elif choice == "11":
        print("Wprowadzony tekst: ", inputText)
        print("Kody: ", letterCodes)
        print("Zakodowany tekst: ", encodedText)
        print("Odkodowany tekst: ", decodedText)
    else:
        break
    input("Aby kontynuować, naciśnij enter...")
