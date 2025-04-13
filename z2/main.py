import serial
from wyslijWiadomosc import wyslijWiadomosc
from odbierzWiadomosc import odbierzWiadomosc
from metodyPomocnicze import wybierzPort, wyborOperacji

print("Implementacja protokołu xModem")

# menu programu
while 1:
    port = wybierzPort() # w pythonie wybieramy port np COM10, a w teraterm ten drugi COM11 lub odwrotnie
    try:
        serialPort = serial.Serial(port, 9600, timeout=10) # wybieramy dany port, predkosc 9600 baud (domyślna i rekomendowana)
        print("Poprawnie połączono z portem.")

        while True:
            menu = wyborOperacji()

            if menu == 1:
                print("Wybrano odbieranie wiadomości.")
                odbierzWiadomosc(serialPort)
                break

            elif menu == 2:
                print("Wybrano wysyłanie wiadomości.")
                calaWiadomosc = input("Wprowadź wiadomość do wysłania: ")
                wyslijWiadomosc(serialPort, calaWiadomosc)
                break

            else:
                print("Wybrano niepoprawną opcję, spróbuj jeszcze raz.")

        serialPort.close()

    except serial.SerialException as e:
        print(e)

    input("Aby kontynuować, naciśnij enter")
