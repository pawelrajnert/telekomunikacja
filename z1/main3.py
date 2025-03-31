from hMatrix import hMatrix
from error import *
from message import *

print("Podaj ciąg znaków do zakodowania:")
mes = str(input())

binaryTable = messageConverterToBinary(mes) # przekształcenie wiadomości do postaci binarnej
encodedMessages = np.array(
    [np.hstack(
        (binaryTable[i], hMatrix[:, :8] @ binaryTable[i] % 2)
    ) for i in range(binaryTable.shape[0])
    ]) # zakodowanie wiadomości - analogicznie jak w main1and2.py
       # binaryTable[i] to po prostu wiadomość, a hMatrix[:, :8] @ binaryTable[i] % 2 - bity kontrolne dla niej

np.savetxt('binaryTable.txt', encodedMessages, fmt="%d", delimiter=',') # zapis do pliku

print("Zasymuluj błąd transmisyjny poprzez zamianę bitów w pliku binaryTable.txt")
print("Program poprawnie rozwiąże problemy, jeśli zmienisz maksymalnie 2 bity w pojedynczej linijce")
print("Pamiętaj o zapisaniu pliku!")
input("Jak dokonasz zmian, naciśnij enter.")

receivedMessage = np.loadtxt('binaryTable.txt', dtype=int, delimiter=',') # odczyt pliku

# weryfikacja wiadomości pod kątem tego, czy nadal jest ona ciągiem bitów
for i in range(receivedMessage.shape[0]):
    stringToVerify = ""
    for j in range(receivedMessage.shape[1]):
        stringToVerify += str(receivedMessage[i][j])    # utworzenie stringa z konkretnych bitów
    fileIsGood = messageVerification(stringToVerify, 1) # właściwa część weryfikacji
    if fileIsGood is False:
        print("Wprowadzone zmiany do pliku binaryTable.txt uniemożliwiają próbę naprawienia błędu transmisyjnego.")
        break

if fileIsGood:
    for i in range(receivedMessage.shape[0]):
        print(f"Linia {i + 1}: ", end="")
        errorCorrector(receivedMessage[i])          # poprawa bitów w otrzymanej wiadomości

    print("Odkodowana wiadomość po korektach: ", end="")
    print(decodeMessage(receivedMessage[:, :8]))
