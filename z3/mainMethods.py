from treePreparation import *
from codeMethods import *
import json


def readTextFile():
    file = input("Podaj nazwę pliku (z rozszerzeniem), z którego odczytamy tekst: ")
    path = f"pliki tekstowe/{file}"
    try:
        openFile = open(path, "r")
        inputText = openFile.read()
        openFile.close()
        if inputText != "":
            print("Pomyślnie wczytano tekst z pliku!")
            return inputText
    except FileNotFoundError:
        print("Wystąpił błąd! Upewnij się, że plik o takiej ścieżce istnieje!")


def encodeData(inputText):
    if inputText != "":
        root, letterOccurrences = prepareTree(inputText)
        letterOccurrences = {key: "" for key in letterOccurrences}
        letterCodes = encodeLetters(letterOccurrences, root, "")
        encodedText = encodeText(inputText, letterCodes)
        print("Tekst wejściowy: ", inputText)
        print("Otrzymałem: ", encodedText)
        print("Wykorzystany słownik: ", letterCodes)
        return letterCodes, encodedText
    else:
        print("Nie wprowadzono tekstu!")
        return {}, ""


def decodeData(letterCodes, encodedText):
    if encodedText != "" or letterCodes != {}:
        decodedText = decodeText(encodedText, letterCodes)
        print("Tekst wejściowy: ", encodedText)
        print("Otrzymałem: ", decodedText)
        print("Wykorzystany słownik: ", letterCodes)
        return decodedText
    else:
        print("Nie zakodowano tekstu lub słownik kodów jest pusty!")
        return ""


def compareTexts(inputText, decodedText):
    if decodedText != "":
        if inputText == "":
            print("Nie jestem w stanie porównać, wprowadzono zakodowany tekst z pliku!")
        elif inputText == decodedText:
            print("Poprawnie odkodowano tekst!")
        else:
            print("Odkodowany tekst jest inny, niż aktualnie wprowadzony")
            print("Wprowadzony tekst - " + inputText)
            print("Odkodowany tekst - " + decodedText)
    else:
        print("Nie jestem w stanie porównać, nie odkodowano tekstu!")


def saveData(letterCodes, encodedText):
    if encodedText != "" and letterCodes != {}:
        try:
            fileName = input("Podaj nazwę pliku (bez rozszerzenia): ")
            path = f"zakodowane/{fileName}.json"
            data = {
                "text": encodedText,
                "codes": letterCodes
            }
            with open(path, "w") as file:
                json.dump(data, file)
        except Exception as e:
            print("Wystąpiły nieoczekiwane błędy przy zapisie - " + str(e))
            return
        print("Udało się zapisać dane do pliku!")
    else:
        print("Brak wystarczających danych do zapisu!")


def readData():
    try:
        fileName = input("Podaj nazwę pliku (bez rozszerzenia): ")
        path = f"zakodowane/{fileName}.json"
        with open(path, "r") as file:
            data = json.load(file)
        encodedText = data["text"]
        letterCodes = data["codes"]
        print("Odczytano pomyślnie!")
        print("Zakodowany tekst: ", encodedText)
        print("Słownik kodów dla niego: ", letterCodes)
        return letterCodes, encodedText
    except FileNotFoundError:
        print("Wystąpił błąd! Upewnij się, że plik o takiej ścieżce istnieje!")
    except json.decoder.JSONDecodeError:
        print("Błąd odczytu danych - niepoprawny format JSON")
    except Exception as e:
        print("Wystąpiły nieoczekiwane błędy przy odczycie - " + str(e))
