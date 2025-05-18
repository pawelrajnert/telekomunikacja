from audio import *


def setValues(initializing):
    def valueValidator(text):
        while True:
            userInput = input(text).strip()
            if userInput == "":
                if initializing:
                    print("Podanie wartości jest wymagane")
                else:
                    return None
            try:
                value = int(userInput)
                if value <= 0:
                    print("Wprowadzona liczba musi być dodatnia.")
                else:
                    return value
            except ValueError:
                print("Nie wprowadzono liczby całkowitej!")

    if not initializing:
        print("Jeśli chcesz pozostawić stare wartości, nie wprowadzaj nic - po prostu wciśnij enter")
    length = valueValidator("Podaj czas nagrania w sekundach: ")
    sampleRate = valueValidator("Podaj częstotliwość próbkowania (Hz): ")
    return length, sampleRate


def menu():
    input_index, output_index = sd.default.device
    usedMicrophone = sd.query_devices(input_index, 'input')
    usedSpeaker = sd.query_devices(output_index, 'output')
    print(
        f"Mikrofon: {usedMicrophone['name']}, "
        f"domyślna częstotliwość próbkowania: {int(usedMicrophone['default_samplerate'])} Hz")
    print(
        f"Odtwarzacz: {usedSpeaker['name']}, "
        f"domyślna częstotliwość próbkowania: {int(usedSpeaker['default_samplerate'])} Hz")
    recordings = []
    l, sr = setValues(True)
    while True:
        print("1. Nagraj dźwięk")
        print("2. Odtwórz dźwięk")
        print("3. Wczytaj pliki z dźwiękami z katalogu")
        print("4. Zmień czas/częstotliwość próbkowania")
        choice = input("Wybierz operację: ")
        if choice == "1":
            ID = len(recordings) + 1
            r = recordSound(l, sr, ID)
            if r is None:
                print(f"Z uwagi na błąd, wymuszam zmianę częstotliwości próbkowania na domyślną wartość mikrofonu "
                      f"{usedMicrophone['name']}: {int(usedMicrophone['default_samplerate'])} Hz")
                sr = int(usedMicrophone['default_samplerate'])
            recordings.append(r)
        elif choice == "2":
            recordingToDelete = chooseRecordingAndPlay(recordings, sr)
            if recordingToDelete is not None:
                print("Z uwagi na błąd, usuwam nagranie z listy nagrań...")
                recordings.remove(recordingToDelete)
        elif choice == "3":
            print("not implemented.")
        elif choice == "4":
            print(l, sr)
            newL, newSr = setValues(False)
            l, sr = newL or l, newSr or sr
            print(l, sr)
