from error import *
from message import messageVerification
from hMatrix import hMatrix

print("Program do poprawiania pojedynczego lub podwójnego błędu transmisji w 8-bitowej wiadomości")
print("Podaj ciąg 8-bitowy do zakodowania: ")

while True:
    mes = str(input())
    if messageVerification(mes, 0):
        break
    else:
        print("Błędna wiadomość, spróbuj ponownie")

message = np.array([int(bit) for bit in mes])  # konwersja bitów do tablicy numpy

controlBits = hMatrix[:,
              :8] @ message % 2  # wyliczenie kontrolnych bitów - iloczyn pierwszych 8 kolumn macierzy h z wiadomością
encodedMessage = np.hstack(
    (message, controlBits))  # utworzenie zakodowanej wiadomości poprzez złączenie wiadomości i bitów kontrolnych
print(f"{encodedMessage} - zakodowana wiadomość")
print("Imitacja błędu transmisyjnego - podaj 16-bitową wiadomość. "
      "Program znajdzie błąd, jeśli podana wiadomość będzie się różniła od zakodowanej 1 lub 2 bitami.")

while True:
    mes = str(input())
    if messageVerification(mes, 1):
        break
    else:
        print("Błędna wiadomość, spróbuj ponownie")

corruptedMessage = np.array([int(bit) for bit in mes])
print(f"{corruptedMessage} - otrzymano taką wiadomość")

errorCorrector(corruptedMessage)  # poprawa błędu

print(f"{corruptedMessage} - stan wiadomości po ewentualnej poprawie")
