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