import numpy as np
from hMatrix import hMatrix as H


# sprawdzanie wystąpienia pojedynczego błędu
# porównujemy wektor błędu do kolejnych kolumn,
# w przypadku znalezienia wektora zwracamy numer kolumny, na której wystąpił pojedynczy błąd
# macierz H ma unikalne kolumny, więc w przypadku pojedynczego błędu metoda powinna być niezawodna

def singleErrorCheck(E):
    for i in range(H.shape[1]):
        if np.array_equal(E, H[:, i]):
            print(f"Pojedynczy błąd na pozycji {i + 1}")
            return i
    else:
        return None


# sprawdzanie wystąpienia pojedynczego błędu
# porównujemy wektor błędu do sumy kolejnych kombinacji dwóch kolumn,
# w przypadku znalezienia jej zwracamy numer kolumn, na których wystąpiły błędy
# na podstawie pliku weryfikacjaMacierzyH.py można wywnioskować,
# że ta metoda również powinna być niezawodna dla podwójnego błędu

def doubleErrorCheck(E):
    for i in range(H.shape[1]):
        for j in range(H.shape[1]):
            if j != i:
                sum = H[:, i] + H[:, j]
                sum %= 2
                if np.array_equal(E, sum):
                    print(f"Podwójny błąd na pozycjach {i + 1}, {j + 1}")
                    return i, j
    else:
        return None


# poprawianie błędu
# na początku wyliczamy wektor błędu. Jeśli jest on zerowy, to nie ma błędu.
# w przeciwnym razie, badamy wystąpienie pojedynczego lub podwójnego błędu transmisji.

def errorCorrector(corruptedMessage):
    errorVector = H @ corruptedMessage % 2
    if sum(errorVector) == 0:
        print("Brak błędu transmisyjnego!")
    else:
        errorPosition = singleErrorCheck(errorVector)
        if errorPosition is not None:
            corruptedMessage[errorPosition] ^= 1  # zmiana wartości bitu przy wykorzystaniu operatora XOR
        else:
            errorPosition = doubleErrorCheck(errorVector)
            if errorPosition is not None:
                corruptedMessage[errorPosition[0]] ^= 1  # zmiana wartości bitu przy wykorzystaniu operatora XOR
                corruptedMessage[errorPosition[1]] ^= 1  # zmiana wartości bitu przy wykorzystaniu operatora XOR
            else:
                print("Nie udało się naprawić błędu transmisyjnego!")
