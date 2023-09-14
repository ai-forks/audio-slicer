import librosa  # Optional. Use any library you like to read audio files.
import soundfile  # Optional. Use any library you like to write audio files.
import re
from slicer2 import Slicer

def main(input: str, options: {threshold: int, min_length:int,min_interval:int, hop_size:int, max_sil_kept:int}):
    audio, sr = librosa.load(input, sr=None, mono=False)  # Load an audio file with librosa.
    options.sr = sr
    options.threshold = options.threshold if options.threshold is not None else -40
    options.min_length = options.min_length if options.min_length is not None else 5000
    options.min_interval = options.min_interval if options.min_interval is not None else 300
    options.hop_size = options.hop_size if options.hop_size is not None else 10
    options.max_sil_kept = options.max_sil_kept if options.max_sil_kept is not None else 500
    slicer = Slicer(
        sr=sr,
        threshold=-40,
        min_length=5000,
        min_interval=300,
        hop_size=10,
        max_sil_kept=500
    )
    chunks = slicer.slice(audio)
    
    input = input.replace("\\", "/")
    name = re.split("/", input)[-1].split(".")[0]
    print(f"name={name}")
    for i, chunk in enumerate(chunks):
        if len(chunk.shape) > 1:
            chunk = chunk.T  # Swap axes if the audio is stereo.
        soundfile.write(f'clips/{name}_{i}.wav', chunk, sr)  # Save sliced audio files with soundfile.
