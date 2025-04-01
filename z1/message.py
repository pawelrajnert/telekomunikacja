import numpy as np


# Weryfikacja wprowadzonej wiadomości, czy na pewno jest ciągiem bitów
# encoded - parametr, który przyjmuje wartość 0 lub 1.
# dla 0 - otrzymana wiadomość ma mieć długość 8 + 0*8 = 8
# dla 1 - otrzymana wiadomość jest zakodowana, ma mieć długość 8 + 8*1 = 16

def messageVerification(mes, encoded):
    if len(mes) == 8 + encoded * 8:
        for i in range(len(mes)):
            if mes[i] not in ('0', '1'):
                return False
        return True
    return False


# konwersja wiadomości z postaci stringa do postaci binarnej
# dzieje sie to na takiej zasadzie, że sprawdzamy kod ascii znaku, i go przekształcamy na postać binarną
# i zwracamy to jako tablicę numpy, zawierającą binarne wektory odpowiednich znaków

def messageConverterToBinary(mes):
    binaryVector = np.array(
        [np.array(
            [int(bit) for bit in format(ord(mes[i]), '08b')]
        ) for i in range(len(mes))
        ])
    return binaryVector


# dekodowanie wiadomości - przekształcamy wektor binarny na kod ascii i na tej podstawie odkodowujemy pojedynczy znak

def decodeMessage(mes):
    decodedMessage = ""
    for i in range(mes.shape[0]):
        asciiChar = 0
        for j in range(mes.shape[1]):
            asciiChar += mes[i][j] * 2 ** (7 - j)
        decodedMessage += chr(asciiChar)
    return decodedMessage
