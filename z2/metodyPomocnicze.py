# definicje znaków sterujących zgodnie z instrukcją
SOH = b'\x01'
EOT = b'\x04'
ACK = b'\x06'
NAK = b'\x15'
CAN = b'\x18'
C = b'C'

znakiSterujace = {
    b'\x01': "SOH",
    b'\x04': "EOT",
    b'\x06': "ACK",
    b'\x15': "NAK",
    b'\x18': "CAN",
    b'C': "C"
}


def wybierzPort():
    wyborPortu = 0

    while wyborPortu not in (1, 2):
        print("Wybierz port na którym chcesz działać: ")
        print("1) Port COM10")
        print("2) Port COM11")
        try:
            wyborPortu = int(input("Wybór: "))
        except ValueError:
            print("Podano niepoprawną wartość. Spróbuj ponownie.")
            continue

        if wyborPortu == 1:
            port = "COM10"

        elif wyborPortu == 2:
            port = "COM11"

        else:
            print("Wybrano niepoprawną opcję, spróbuj jeszcze raz.")

    return port


# wybor sumy kontrolnej/algorytmu CRC przez użytkownika
def wyborSumyKontrolnej():
    while True:
        print("Wybierz z której sumy kontrolnej chcesz korzystać: ")
        print("1) suma kontrolna")
        print("2) algorytm CRC")
        wybor = int(input("Wybór: "))
        if wybor == 1:
            print("Wybrano sumę kontrolną.")
            return True

        elif wybor == 2:
            print("Wybrano algorytm CRC.")
            return False

        else:
            print("Wybrano niepoprawną opcję, spróbuj jeszcze raz.")


# wybór operacji - nadanie/odebranie wiadomości.
def wyborOperacji():
    print("Wybierz co chcesz zrobić: ")
    print("1) Odbierz wiadomość")
    print("2) Wyślij wiadomość")
    menu = int(input("Wybierz opcję: "))
    return menu


# dodajemy wartości ASCII każdego znaku w bloku i jeżeli wartość jest większa niż 256
# lub wielokrotności 256 to odejmujemy właśnie tyle- tak się tworzy sumę kontrolną
# np. suma znaków to 312 > 256 zatem odejmujemy 256 i wychodzi nam suma kontrolna 56
def sumaKontrolna(blokWiadomosci):
    suma = sum(blokWiadomosci)

    while suma > 256:
        suma -= 256

    return suma


# suma kontrolna obliczona na podstawie algorytmu CRC
def algorytmCRC(blokWiadomosci):
    crc = 0
    # dzielnik dla wersji CRC16 (dla protokołu xModem)
    dzielnik = 0x1021

    for bajt in blokWiadomosci:
        crc ^= (bajt << 8)

        for i in range(8):
            if crc & 0x8000:  # sprawdzamy czy bit najbardziej po lewo jest ustawiony na 1
                crc = (crc << 1) ^ dzielnik  # jesli jest on rowny 1 to przesuwamy w lewo o 1 i robimy xor z dzielnikiem

            else:
                crc = crc << 1  # jesli bit nie wynosi 1 to przesuwamy w lewo o 1

            crc &= 0xFFFF  # maska 16 bit aby zapewnić że crc bedzie mialo wlasnie tyle bitow

    return crc


# funkcja dopełniająca wiadomość do pełnych 128 bajtów (lub wielokrotności)
def rowneBloki(calaWiadomosc):
    blokiDoDopelnienia = len(calaWiadomosc) % 128  # sprawdzamy ile bajtow brakuje nam co pełnych 128 lub wielokrotności

    if blokiDoDopelnienia != 0:
        ileDopelnic = 128 - blokiDoDopelnienia  # dopelniamy spacjami do pelnych bajtow
        calaWiadomosc += ' ' * ileDopelnic

    return calaWiadomosc


# funkcja podziału wiadomości na bloki o rozmiarze 128 bajtow
def podzielWiadomosc(calaWiadomosc):
    calaWiadomosc = rowneBloki(calaWiadomosc)  # najpierw dopełniamy bloki do pełnych 128 bajtów
    blokiWiadomosci = []

    for i in range(0, len(calaWiadomosc), 128):  # sprawdzamy i dzielimy wiadomosc na 128 bajtowe bloki
        blok = calaWiadomosc[i:i + 128]  # bierzemy każdy blok 128 bajtów
        blokiWiadomosci.append(blok)  # i dodajemy go do tablicy

    return blokiWiadomosci