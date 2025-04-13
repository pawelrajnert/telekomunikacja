import serial
import time

# definicje znaków sterujących zgodnie z instrukcją
SOH = b'\x01'
EOT = b'\x04'
ACK = b'\x06'
NAK = b'\x15'
CAN = b'\x18'
C   = b'C'

print("Implementacja protokołu xModem")

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


def wyslijWiadomosc(port, calaWiadomosc, typSumyKontrolnej):
    bloki = podzielWiadomosc(calaWiadomosc)

    waitForConnection = time.time()
    receivedSignal = None
    while time.time() - waitForConnection < 60:
        if port.in_waiting > 0: # jeśli w buforze znajdzie się jakaś dana (bajt)
            inBufferSignal = port.read(1) # odczytujemy ten bajt
            if inBufferSignal in [NAK, C]: # jeśli jest to NAK lub C, to wychodzimy z pętli
                # NAK - suma kontrolna, C - suma kontrolna z algorytmem CRC
                receivedSignal = inBufferSignal
                break
        time.sleep(1)

    if receivedSignal is None:
         print("Nie otrzymano oczekiwanej odpowiedzi NAK lub C.")
         return

    else:
        print("Otrzymano oczekiwany komunikat: ", receivedSignal)

    numerBloku = 1
    for blok in bloki:
        blok = blok.encode('ascii')
        nrBloku = numerBloku.to_bytes(1)
        nrDopełnienia = (255 - numerBloku).to_bytes(1)
        if typSumyKontrolnej: suma = sumaKontrolna(blok).to_bytes(1)
        else: suma = algorytmCRC(blok).to_bytes(2)
        pakiet = SOH + nrBloku + nrDopełnienia + blok + suma
        port.write(pakiet)
        waitForConnection = time.time()
        time.sleep(1) # Tak by na pewno odczytać dobry znak
        while time.time() - waitForConnection < 5: # dajemy 5 sekund na odpowiedź
            if port.in_waiting > 0:  # jeśli w buforze znajdzie się jakaś dana (bajt)
                receivedSignal = port.read(1)  # odczytujemy ten bajt
                if receivedSignal == ACK:  # jeśli jest to NAK lub C, to wychodzimy z pętli
                    # NAK - suma kontrolna, C - suma kontrolna z algorytmem CRC
                    print("Odbiorca potwierdził poprawność, przechodzę do kolejnego bloku")
                    numerBloku += 1
                    break
                elif receivedSignal == NAK:
                    print("Odbiorca zgłosił błąd, ponawiam wysłanie bloku")
                    port.write(pakiet)
                elif receivedSignal == CAN:
                    print("Odbiorca anulował transmisję...")
                    return
                else: print("Odbiorca odpowiedział nieoczekiwanie: " + str(receivedSignal))
            time.sleep(0.2)
    print("Koniec transmisji, zgłaszam to odbiorcy")
    port.write(EOT)
    time.sleep(1)
    waitForConnection = time.time()
    while time.time() - waitForConnection < 5:
        if port.in_waiting > 0:
            receivedSignal = port.read(1)
            if receivedSignal == ACK:
                print("Odbiorca potwierdził poprawne zakończenie transmisji")
                return
        time.sleep(0.1)
        port.write(EOT)
    print("Ponowne wysyłanie komunikatu nie przyniosło oczekiwanego efektu, kończę transmisję bez reakcji z drugiej strony...")

def odbierzWiadomosc(port, typSumyKontrolnej):
    waitForConnection = time.time()
    receivedSignal = None

    def rozpocznijTransmisję():
        if typSumyKontrolnej: port.write(NAK)
        else: port.write(C)

    def zweryfikujSumęKontrolną(rs):
        if typSumyKontrolnej:
            suma = port.read(1)
            return suma == sumaKontrolna(rs).to_bytes(1)
        else:
            suma = port.read(2)
            return suma == algorytmCRC(rs).to_bytes(2)

    while waitForConnection - time.time() < 60:
        rozpocznijTransmisję()
        time.sleep(10)
        if port.in_waiting > 0:
            inBufferSignal = port.read(1)
            if inBufferSignal == SOH:
                receivedSignal = inBufferSignal
                break
            else:
                print("Anuluję transmisję, otrzymano nieoczekiwany komunikat: " + str(receivedSignal))
                return

    if receivedSignal is None:
        print("Nie otrzymano oczekiwanej odpowiedzi SOH, zakończono oczekiwanie.")
        return
    else:
        print("Otrzymano komunikat: ", receivedSignal)
    numerBloku = 1
    błądTransmisji = [False, ""]
    while True:
        błądTransmisji[0] = False
        if port.in_waiting > 0:
            receivedSignal = port.read(1)
            if receivedSignal == EOT:
                break
            if receivedSignal != numerBloku.to_bytes(1):
                błądTransmisji = [True, "Nieprawidłowy numer bloku!"]
                break
            receivedSignal = port.read(1)
            if receivedSignal != (255 - numerBloku).to_bytes(1):
                błądTransmisji = [True, "Nieprawidłowa liczba dopełnienia"]
                break
            receivedSignal = port.read(128)
            print(str(numerBloku) + " blok - otrzymane dane: " + receivedSignal.decode('ascii', errors='ignore'))
            if zweryfikujSumęKontrolną(receivedSignal) is False:
                błądTransmisji = [True, "Nieprawdiłowa suma kontrolna/CRC"]
            if błądTransmisji[0]:
                print(błądTransmisji[1] + " - wysyłam komunikat NAK")
                port.write(NAK)
            else:
                port.write(ACK)
                print("Suma kontrolna/CRC się zgadza - wysyłam komunikat ACK")
    if błądTransmisji[0]:
        print("Anuluję transmisję: " + błądTransmisji[1])
        port.write(CAN)
    else:
        print("Przesyłam komunikat ACK, by zakończyć transmisję")
        port.write(ACK)



# menu programu
while 1:
    port = wybierzPort() # w pythonie wybieramy port np COM10, a w teraterm ten drugi COM11 lub odwrotnie
    try:
        serialPort = serial.Serial(port, 9600, timeout=10) # wybieramy dany port, predkosc 9600 baud (domyślna i rekomendowana)
        print("Poprawnie połączono z portem.")
    except serial.SerialException as e:
        print(e)

    print("Wybierz co chcesz zrobić: ")
    print("1) Odbierz wiadomość")
    print("2) Wyślij wiadomość")
    menu = int(input("Wybierz opcję: "))

    if menu == 1:
        print("Wybrano odbieranie wiadomości.")
        suma = wyborSumyKontrolnej()
        if suma == True:
            print("Wybrano sumę kontrolną.")
            odbierzWiadomosc(serialPort, suma)
        if suma == False:
            print("Wybrano algorytm CRC")
            odbierzWiadomosc(serialPort, suma)

    elif menu == 2:
        print("Wybrano wysyłanie wiadomości.")
        suma = wyborSumyKontrolnej()
        if suma == True:
            print("Wybrano sumę kontrolną.")
            calaWiadomosc = input("Wprowadź wiadomość do wysłania: ")
            wyslijWiadomosc(serialPort, calaWiadomosc, suma)

        if suma == False:
            print("Wybrano algorytm CRC")
            calaWiadomosc = input("Wprowadź wiadomość do wysłania: ")
            wyslijWiadomosc(serialPort, calaWiadomosc, suma)

    else:
        print("Wybrano niepoprawną opcję, spróbuj jeszcze raz.")

    serialPort.close()
    input("Aby kontynuować, naciśnij enter")
