from hMatrix import hMatrix as H

# Metoda niewykorzystywana w programie, napisana w celu weryfikacji macierzy H - a konkretniej sumy 2 kolumn

unikaty = set()
for i in range(H.shape[1]):
    kolumna = H[:, i]
    unikaty.add(tuple(kolumna))
    for j in range(i + 1, H.shape[1]):
        suma = H[:, i] + H[:, j]
        suma %= 2
        if sum(suma) != 0:
            unikaty.add(tuple(suma))
print(len(unikaty))
# unikalnych połączeń jest 120 + 16 kolumn - jeśli na ekranie ukaże się 136 to macierz H jest poprawna do poprawy 2 błędów

# metody do sprawdzania unikalności kolumn nie napisaliśmy,
# ale jest to dużo prostsze do weryfikacji niż unikalne sumy 136 kombinacji
