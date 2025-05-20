import numpy as np


def snrFunction(r):
    if len(r) <= 1:
        print("Za mało nagrań do obliczenia SNR!")
        return
    recordingNames = list(r.keys())
    bestRecordingName = determineBestRecording(recordingNames)
    print(f"Najlepsze nagranie: {bestRecordingName}")
    print("Wyliczone wartości:")
    for record in recordingNames:
        if record == bestRecordingName:
            continue
        result = calculateSNR(r[bestRecordingName], r[record])
        print(f"{record} -> {result:.3f} dB")


def determineBestRecording(names):
    bestRecording = ""
    bestScore = 0
    for name in names:
        cutName = name[:-6]
        nameParts = cutName.split("_")
        bits = int(nameParts[3])
        sampleRate = int(nameParts[4])
        score = bits * sampleRate
        if score > bestScore:
            bestScore = score
            bestRecording = name
    return bestRecording

def calculateSNR(baseSignal, testSignal):
    # Wykorzystany wzór: SNR = 10 * log10(x/y),
    # gdzie: x — uśredniona wartość np.array z oryginalnym sygnałem podniesionym do kwadratu,
    # y — uśredniona wartość np.array szumu (różnica oryginalnego dźwięku i przetworzonego) podniesionego do kwadratu

    length = min(len(baseSignal), len(testSignal))  # przycięcie, by tablice miały ten sam rozmiar
    baseSignal = baseSignal[:length]
    testSignal = testSignal[:length]

    noise = baseSignal - testSignal                 # obliczenie szumu
    basePower = np.mean(baseSignal ** 2)            # obliczenie x ze wzoru
    noisePower = np.mean(noise ** 2)                # obliczenie y ze wzoru

    try:
        snr = 10 * np.log10(basePower / noisePower)
    except ZeroDivisionError:
        return np.inf
    return snr