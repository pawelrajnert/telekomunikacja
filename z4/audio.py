import sounddevice as sd
from file import *


def recordSound(recordingLength, sampleRate, ID, bits):
    try:
        print(f"Rozpoczęto nagrywanie, czas nagrania: {recordingLength}s")
        recording = sd.rec(frames=int(recordingLength * sampleRate), samplerate=sampleRate, channels=1, dtype='float32')
        sd.wait()
        print("Zakończono nagrywanie")
        recordingName = f"recording_{ID}_{recordingLength}s_{bits}_{sampleRate}Hz.wav"
        print("Czy chcesz zapisać nagranie do katalogu? (t/n)")
        while True:
            choice = input().strip().lower()
            if choice == "t" or choice == "T":
                saveToFile(recording, recordingName, sampleRate, bits)
                break
            elif choice == "n" or choice == "N":
                break
            else:
                print("Niepoprawny wybór (t/n)")
        return recording, recordingName
    except Exception as e:
        print("Wystąpił błąd: " + str(e))
        return None


def playSound(recording, name):
    name = name[:-6]
    nameParts = name.split("_")
    sampleRate = int(nameParts[4])
    try:
        print("Odtwarzam nagranie...")
        sd.play(recording, sampleRate)
        sd.wait()
        print("Zakończono odtwarzanie!")
        return False
    except Exception as e:
        print("Nie można odtworzyć nagrania: " + str(e))
        return True


def chooseRecordingAndPlay(recs):
    names = list(recs.keys())
    if len(recs) > 0:

        print("Wybierz numer z listy nagrań: ")
        for i, name in enumerate(names):
            print(f"{i + 1}. - " + name)
    else:
        print("Lista nagrań jest pusta!")
        return None
    while True:
        try:
            choice = int(input().strip().lower())
            if 1 <= choice <= len(recs):
                name = names[choice - 1]
                errorHasOccurred = playSound(recs[name], name)
                if errorHasOccurred:
                    return name
                else:
                    return None
            else:
                print("Numer poza zakresem!")
        except ValueError:
            print("Wprowadź prawidłowy numer z listy")
