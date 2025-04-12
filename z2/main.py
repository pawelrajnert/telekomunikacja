# definicje znaków sterujących zgodnie z instrukcją
SOH = 0x01
EOT = 0x04
ACK = 0x06
NAK = 0x15
CAN = 0x18
C = 0x43

print("Implementacja protokołu xModem")


# wybor sumy kontrolnej/algorytmu CRC przez użytkownika
def wyborSumyKontrolnej():
    print("Wybierz z której sumy kontrolnej chcesz korzystać: ")
    print("1) suma kontrolna")
    print("2) algorytm CRC")
    wybor = int(input("Wybór: "))
    if wybor == 1:
        print("Wybrano odbieranie wiadomości.")
        suma = True

    elif wybor == 2:
        print("Wybrano wysyłanie wiadomości.")
        suma = False

    else:
        print("Wybrano niepoprawną opcję, spróbuj jeszcze raz.")

    return suma


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


# menu programu
while 1:
    print("Wybierz co chcesz zrobić: ")
    print("1) Odbierz wiadomość")
    print("2) Wyślij wiadomość")
    menu = int(input("Wybierz opcję: "))

    if menu == 1:
        print("Wybrano odbieranie wiadomości.")
        suma = wyborSumyKontrolnej()
        if suma == True:
            print("Wybrano sumę kontrolną.")
        if suma == False:
            print("Wybrano algorytm CRC")

    elif menu == 2:
        print("Wybrano wysyłanie wiadomości.")
        suma = wyborSumyKontrolnej()
        if suma == True:
            print("Wybrano sumę kontrolną.")
        if suma == False:
            print("Wybrano algorytm CRC")

    else:
        print("Wybrano niepoprawną opcję, spróbuj jeszcze raz.")

    input("Aby kontynuować, naciśnij enter")
