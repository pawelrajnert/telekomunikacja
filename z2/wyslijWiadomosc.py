import time
from metodyPomocnicze import *


# Schemat wysyłania wiadomości:
# Nawiązaliśmy połączenie z portem szeregowym. Zakładamy, że odbiorca też się już połączył/połączy się.
# Na samym początku ustawiamy pierwszy timer. Dajemy odbiorcy 60 sekund na wysłanie komunikatu NAK lub C
# Obydwa z nich oznaczają, że odbiorca jest gotowy; w pierwszym przypadku korzysta on z sumy kontrolnej, w drugim — z CRC.
# Komunikaty odbieramy co sekundę. Gdy odbierzemy komunikat NAK lub C, to weryfikujemy, czy mamy zgodność co do oczekiwań
# — tzn. czy użytkownik i odbiorca razem wskazują sumę kontrolną/CRC.
# W przypadku niezgodności anulujemy transmisję.
# Wiadomości przesyłamy blok po bloku. Schemat pojedynczej wiadomości:
# SOH + nrBloku + nrDopełnienia + wiadomość + suma kontrolna/CRC, zatem 1 bajt + 1 bajt + 1 bajt + 128 bajtów + 1/2 bajty
# nrDopełnienia + nrBloku mają razem dawać 255 (FF), odbiorca sobie to weryfikuje.
# Następnie czekamy na odpowiedź ze strony odbiorcy:
# - ACK — wszystko przebiegło dobrze — przechodzimy do kolejnego bloku,
# - NAK — wystąpiła niezgodność — przesyłamy ponownie ten sam bloku,
# - CAN — odbiorca anulował transmisję, kończymy przesyłanie,
# - jakiś inny sygnał — wyświetlamy go na ekranie.
# Dajemy odbiorcy 5 sekund na odpowiedź, a odczytujemy jego odpowiedź co 0,2 sekundy.
# Jeśli dotrzemy do ostatniego bloku, to wysyłamy komunikat EOT — koniec transmisji, na który odbiorca ma odpowiedzieć ACK.
# Ponownie dajemy mu na to 5 sekund, a tym razem co 0,1 sekundy będziemy wysyłać komunikat EOT.
# Jeśli nie otrzymamy odpowiedzi w ciągu 5 sekund, po prostu kończymy transmisję.

def wyslijWiadomosc(port, calaWiadomosc):
    bloki = podzielWiadomosc(calaWiadomosc)  # dzielimy wiadomość na bloki
    typSumyKontrolnej = wyborSumyKontrolnej()  # wybieramy sumę kontrolną
    waitForConnection = time.time()  # pobieramy czas rozpoczęcia
    receivedSignal = None

    while time.time() - waitForConnection < 60:
        if port.in_waiting > 0:  # jeśli w buforze znajdzie się jakaś dana (bajt)
            inBufferSignal = port.read(1)  # odczytujemy ten bajt
            if inBufferSignal in [NAK, C]:  # jeśli jest to NAK lub C, to wychodzimy z pętli
                # NAK - suma kontrolna, C - suma kontrolna z algorytmem CRC
                receivedSignal = inBufferSignal
                break
        time.sleep(1)

    if receivedSignal is None:
        print("Nie otrzymano oczekiwanej odpowiedzi NAK lub C.")
        return

    elif receivedSignal == C and typSumyKontrolnej:  # weryfikujemy zgodność co do oczekiwań
        print("Odbiorca oczekuje CRC, a wskazano sumę kontrolną - anuluję transmisję.")
        port.write(CAN)
        port.write(CAN)
        return

    elif receivedSignal == NAK and not typSumyKontrolnej:  # weryfikujemy zgodność co do oczekiwań
        print("Odbiorca oczekuje sumy kontrolnej, a wskazano CRC - anuluję transmisję.")
        port.write(CAN)
        port.write(CAN)
        return

    else:
        print("Otrzymano oczekiwany komunikat: ", znakiSterujace.get(receivedSignal, str(receivedSignal)) + ", przechodzę do transmisji.")

    numerBloku = 1  # od 1 bloku idziemy
    for Blok in bloki:  # dla każdego bloku
        blokBajty = Blok.encode('ascii')  # kodujemy blok na ASCII
        nrBloku = numerBloku.to_bytes(1)  # przekształcenie na bajty
        nrDopełnienia = (255 - numerBloku).to_bytes(1)  # przekształcenie na bajty

        if typSumyKontrolnej:
            suma = sumaKontrolna(blokBajty).to_bytes(1)  # przekształcenie na bajty sumy kontrolnej

        else:
            suma = algorytmCRC(blokBajty).to_bytes(2)  # przekształcenie na 2(!) bajty CRC

        pakiet = SOH + nrBloku + nrDopełnienia + blokBajty + suma  # utworzenie pakietu do wysłania
        print("Przesyłam blok: " + str(numerBloku) + " - " + Blok)
        port.write(pakiet)  # wysłanie pakietu
        time.sleep(1)  # Dajemy czas na reakcję, by nie odczytać znaku złego znaku
        waitForConnection = time.time()

        while time.time() - waitForConnection < 5:  # dajemy 5 sekund na odpowiedź
            if port.in_waiting > 0:  # jeśli w buforze znajdzie się jakaś dana (bajt)
                receivedSignal = port.read(1)  # odczytujemy ten bajt
                if receivedSignal == ACK:  # jeśli jest to ACK, to odbiorca zgłosił poprawność
                    print("Odbiorca potwierdził poprawność (ACK), przechodzę do kolejnego bloku")
                    numerBloku += 1  # kolejny blok
                    numerBloku %= 256  # bo numer bloku to liczba 8 bitowa - zakres 0-255
                    break  # przerywamy pętle

                elif receivedSignal == NAK:  # nastąpił błąd zgłoszony przez odbiorcę
                    print("Odbiorca zgłosił błąd (NAK), ponawiam wysłanie bloku")
                    port.write(pakiet)  # ponowne wysłanie bloku

                elif receivedSignal == CAN:  # anulowanie transmisji
                    print("Odbiorca anulował transmisję (CAN)...")
                    port.write(CAN)
                    port.write(CAN)
                    return

                else:
                    print("Odbiorca odpowiedział nieoczekiwanie: " + znakiSterujace.get(receivedSignal, str(receivedSignal)))  # dla nieoczekiwanych komunikatów

            time.sleep(0.2)
    print("Koniec transmisji, zgłaszam to odbiorcy")
    port.write(EOT)  # kończymy transmisję
    time.sleep(1)  # Dajemy czas na reakcję, by nie odczytać znaku złego znaku
    waitForConnection = time.time()

    while time.time() - waitForConnection < 5:  # dajemy 5 sekund na odpowiedź
        if port.in_waiting > 0:  # jeśli w buforze znajdzie się jakaś dana (bajt)
            receivedSignal = port.read(1)  # odczytujemy ten bajt
            if receivedSignal == ACK:  # oczekujemy na ACK - potwierdzenie zakończenia transmisji
                print("Odbiorca potwierdził poprawne zakończenie transmisji (ACK)")
                return

        time.sleep(0.1)  # co 0.1 sekundy ponawiamy komunikat o końcu transmisji
        print("Ponawiam przesłanie EOT...")
        port.write(EOT)

    print("Ponowne wysyłanie komunikatu nie przyniosło oczekiwanego efektu, kończę transmisję bez reakcji z drugiej strony...")