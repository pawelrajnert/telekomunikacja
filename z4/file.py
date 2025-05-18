import os
import soundfile as sf


def saveToFile(recording, name, sampleRate, bits):
    try:
        os.makedirs("nagrania", exist_ok=True)
        path = f"nagrania/{name}.wav"
        types = {
            8: 'PCM_U8',
            16: 'PCM_16',
            24: 'PCM_24',
            32: 'PCM_32'
        }
        sf.write(path, recording, sampleRate, types[bits])
        print(f"Zapisano dane do pliku: {path}")
    except Exception as e:
        print("Błąd zapisu: " + str(e))


def properFileName(file):
    if not file.endswith("Hz.wav"): return False
    fileParts = file[:-4].split("_")  # obcięcie .wav i podzielenie po _
    try:
        # sprawdzenie ilości części
        if len(fileParts) != 5: return False

        # sprawdzenie początku nazwy
        if fileParts[0] != "recording": return False

        # sprawdzenie numeru porządkowego - ma być intem
        identifier = int(fileParts[1])
        if identifier < 0: return False

        # Sprawdzenie czasu trwania - np. 5s
        if not fileParts[2].endswith("s"): return False
        duration = int(fileParts[2][:-1])
        if duration < 0: return False

        # sprawdzenie poziomu kwantyzacji
        properValues = [8, 16, 24, 32]
        fileValue = int(fileParts[3])
        if fileValue not in properValues: return False

        # sprawdzenie częstotliwości
        if not fileParts[4].endswith("Hz"): return False
        sampleRate = int(fileParts[4][:-2])
        if sampleRate < 0: return False

    except ValueError:
        return False
    return True


def loadAudio(r):
    files = os.listdir("nagrania")
    for file in files:
        if file in r or not properFileName(file): continue
        recording = sf.read("nagrania/" + file)
        data = recording[0]
        r[file] = data
        print(f"Załadowane dane z pliku: {file}")
    return r
