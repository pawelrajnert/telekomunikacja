from treePreparation import *
from codeMethods import *
import json
import socket


def readTextFile():
    file = input("Podaj nazwę pliku txt (bez rozszerzenia), z którego odczytamy tekst: ")
    path = f"pliki tekstowe/{file}.txt"
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
            print("Wprowadzony tekst i odkodowany są takie same!")
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


def saveText(decodedText):
    if decodedText != "":
        try:
            fileName = input("Podaj nazwę pliku do zapisu (bez rozszerzenia): ")
            path = f"odkodowane/{fileName}.txt"
            with open(path, "w") as file:
                file.write(decodedText)
                file.close()
        except Exception as e:
            print("Wystąpiły nieoczekiwane błędy przy zapisie - " + str(e))
    else:
        print("Nie można zapisać - brak odkodowanego tekstu!")


def sendData(letterCodes, encodedText):
    if encodedText != "" and letterCodes != {}:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ip = input("Podaj ip odbiorcy: ")
            port = int(input("Podaj port odbiorcy: "))
            s.connect((ip, int(port)))
            data = {
                "text": encodedText,
                "codes": letterCodes
            }
            s.sendall(json.dumps(data).encode("utf-8"))
            print("Przesłano dane!")
        except socket.error as e:
            print("Wystąpił błąd z gniazdem: " + str(e))
        except Exception as e:
            print("Wystąpił nieoczekiwany błąd: " + str(e))
        finally:
            s.close()
    else:
        print("Brak wystarczających danych do przesłania!")


def receiveData():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = None
    try:
        port = int(input("Podaj port nasłuchiwania: "))
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print("Oczekuje na dane na porcie: " + str(port))

        conn, addr = s.accept()
        print("Połączono z: " + str(addr))
        data = b""
        while True:
            receivedBytes = conn.recv(1024)
            if not receivedBytes:
                break
            data += receivedBytes
        decodedData = json.loads(data.decode("utf-8"))
        letterCodes = decodedData["codes"]
        encodedText = decodedData["text"]
        print("Odebrano dane z drugiego komputera!")
        return letterCodes, encodedText
    except socket.error as e:
        print("Wystąpił błąd z gniazdem: " + str(e))
    except json.decoder.JSONDecodeError as e:
        print("Błąd odczytu danych - niepoprawny format JSON: " + str(e))
    except Exception as e:
        print("Wystąpił nieoczekiwany błąd: " + str(e))
    finally:
        conn.close()
        s.close()
