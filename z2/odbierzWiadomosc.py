import time
from metodyPomocnicze import *

# Ogólny schemat został przedstawiony w pliku wyslijWiadomosc.py, tutaj skrócony opis od drugiej strony:
# - wysyłamy NAK (suma kontrolna) lub C (CRC) co 10 sekund,
# - jeśli mamy coś do odczytania, odczytujemy 1 bajt — jeśli to SOH, to zaczynamy czytać blok,
# - odczytujemy 1 bajt — nrBloku, i go weryfikujemy,
# - odczytujemy 1 bajt — nrDopełnienia, i go weryfikujemy,
# - odczytujemy 128 bajtów — wiadomość — i wyliczamy sumę kontrolną,
# - odczytujemy 1/2 bajty — suma kontrolna/CRC — porównujemy z obliczoną sumą kontrolną/CRC
# Następnie odpowiadamy odbiorcy:
# - ACK — nie nastąpił żaden błąd, sumy kontrolne się zgadzają — przechodzimy dalej,
# - NAK — wystąpił błąd jakiś, czekamy na ponowne przesłanie bloku.
# - CAN — otrzymano nieoczekiwany komunikat/nie zgadza się nrBloku/nrDopełnienia — anulujemy transmisję.
# Jeśli natomiast zamiast SOH odczytamy EOT, to odpowiadamy odbiorcy ACK, by zakończyć transmisję.

def odbierzWiadomosc(port):
    waitForConnection = time.time()             # czas początkowy
    receivedSignal = None                       # odebrane sygnały
    typSumyKontrolnej = wyborSumyKontrolnej()   # True - suma kontrolna, False - CRC

    def rozpocznijTransmisję():
        if typSumyKontrolnej:
            port.write(NAK)
        else:
            port.write(C)

    def zweryfikujSumęKontrolną(rs):
        if typSumyKontrolnej:
            suma = port.read(1)                                 # bo 1 bajt - 8 bitów
            return suma == sumaKontrolna(rs).to_bytes(1)        # przyrównujemy sumę kontrolną do metody weryfikującej
        else:
            suma = port.read(2)                                 # bo 2 bajty - 16 bitów
            return suma == algorytmCRC(rs).to_bytes(2)          # przyrównujemy sumę kontrolną do metody weryfikującej

    while time.time() - waitForConnection < 60:                 # będziemy czekać 60 sekund
        rozpocznijTransmisję()                                  # przesyłamy stosowny komunikat
        time.sleep(10)                                          # czekamy 10 sekund
        if port.in_waiting > 0:                                 # odczytujemy komunikat — jeśli jest
            inBufferSignal = port.read(1)
            if inBufferSignal == SOH:                           # oczekujemy SOH
                receivedSignal = inBufferSignal
                break
            elif inBufferSignal == CAN:
                print("Transmisja została anulowana przez nadawcę!")
                port.write(CAN)
                port.write(CAN)
                return
            else:
                print("Anuluję transmisję, otrzymano nieoczekiwany komunikat: " + str(inBufferSignal))
                port.write(CAN)
                port.write(CAN)
                return

    if receivedSignal is None:
        print("Nie otrzymano oczekiwanej odpowiedzi SOH, zakończono oczekiwanie.")
        return
    else:
        print("Otrzymano komunikat: ", receivedSignal)
    numerBloku = 1
    błądTransmisji = [False, ""]                    # tutaj przechowujemy komunikat błędu, jeśli zdecydujemy się anulować transmisję
    while True:
        if port.in_waiting > 0:                 # odczytujemy tylko wtedy, gdy mamy co
            if receivedSignal != SOH:               # odczytujemy nagłówek dla ponownego przejścia pętli
                receivedSignal = port.read(1)
                print("Otrzymano komunikat: ", receivedSignal)
                if receivedSignal == EOT:  # koniec transmisji, wychodzimy bez błędu.
                    break
                elif receivedSignal == CAN:  # na wypadek anulowania transmisji
                    błądTransmisji = [True, "Nadawca anulował transmisję!"]
                    break
                elif receivedSignal != SOH:     # w innym wypadku, anulujemy transmisję
                    błądTransmisji[1] = "Nie otrzymano oczekiwanego komunikatu SOH!"
                    break
                else: błądTransmisji[0] = False # reset flagi błędu
            receivedSignal = port.read(1)       # odczytujemy 1 bajt
            if receivedSignal != numerBloku.to_bytes(1):        # weryfikujemy informacje o numerze bloku
                błądTransmisji = [True, "Nieprawidłowy numer bloku!"]
                break
            receivedSignal = port.read(1)       # odczytujemy numer dopełnienia
            if receivedSignal != (255 - numerBloku).to_bytes(1):    # weryfikujemy go
                błądTransmisji = [True, "Nieprawidłowa liczba dopełnienia"]
                break
            receivedSignal = port.read(128)         # odczytujemy dane, wyliczamy ich sumę kontrolną zaraz
            print(str(numerBloku) + " blok - otrzymane dane: " + receivedSignal.decode('ascii', errors='ignore'))
            if zweryfikujSumęKontrolną(receivedSignal) is False:        # weryfikacja sumy kontrolnej/crc
                błądTransmisji = [True, "Nieprawdiłowa suma kontrolna/CRC"]
            if błądTransmisji[0]:           # nastąpił błąd - przesyłamy NAK
                print(błądTransmisji[1] + " - wysyłam komunikat NAK")
                port.write(NAK)
            else:           # jeśli nie wystąpił błąd transmisji
                print("Suma kontrolna/CRC się zgadza - wysyłam komunikat ACK")
                port.write(ACK)
                numerBloku += 1     # zwiększamy numerBloku o 1
                numerBloku %= 256   # bo numer bloku to liczba 8 bitowa - zakres 0-255

    if błądTransmisji[0]:           # z jakiegoś powodu musimy anulować transmisję
        print("Anuluję transmisję: " + błądTransmisji[1])
        port.write(CAN)
        port.write(CAN)
    else:       # tylko w wypadku, gdy otrzymaliśmy EOT
        print("Przesyłam komunikat ACK, by zakończyć transmisję")
        port.write(ACK)