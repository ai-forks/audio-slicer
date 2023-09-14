import librosa  # Optional. Use any library you like to read audio files.
import soundfile  # Optional. Use any library you like to write audio files.
import re
from slicer2 import Slicer
import argparse
import logging
import os
import glob


logging.basicConfig(format="[autocut:%(filename)s:L%(lineno)d] %(levelname)-6s %(message)s")
logging.getLogger().setLevel(logging.INFO)

def main():
    parser = argparse.ArgumentParser(
        description="Edit videos based on transcribed subtitles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        help="intpu files",
        type=int,
        default=-40
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="The RMS threshold presented in dB. Areas where all RMS values are below this threshold will be regarded as silence. Increase this value if your audio is noisy. Defaults to -40",
        type=int,
        default=-40
    )
    parser.add_argument(
        "-ml",
        "--min_length",
        help="The minimum length required for each sliced audio clip, presented in milliseconds. Defaults to 5000",
        type=int,
        default=5000
    )

    parser.add_argument(
        "-mi",
        "--min_interval",
        help=("The minimum length for a silence part to be sliced, presented in milliseconds. Set this value smaller if your audio contains only short breaks. The smaller this value is, the more sliced audio clips this script is likely to generate. Note that this value must be smaller than min_length and larger than hop_size. Defaults to 300."),
        type=int,
        default=300
    )
    parser.add_argument(
        "-hs",
        "--hop_size",
        help=("Length of each RMS frame, presented in milliseconds. Increasing this value will increase the precision of slicing, but will slow down the process. Defaults to 10."),
        type=int,
        default=10
    )
    parser.add_argument(
        "-msk",
        "--max_sil_kept",
        help=("The maximum silence length kept around the sliced audio, presented in milliseconds. Adjust this value according to your needs. Note that setting this value does not mean that silence parts in the sliced audio have exactly the given length. The algorithm will search for the best position to slice, as described above. Defaults to 1000."),
        type=int,
        default=1000
    )
    args = parser.parse_args()

    if os.path.isfile(args.input) :
        handle(args.input, args)
    elif os.path.isdir(args.input) :
        dir = args.input
        files = glob.glob(dir+"/*.(mp3|wav|flac)")
        print(f"files={files}")
        for i, name in files:
            handle(os.path.join(dir, name), args)

    
    
def handle(file: string, args: {
    threshold:int,
    min_length:int,
    min_interval:int,
    hop_size:int,
    max_sil_kept:int}
):
    print(f"handle==={file}")
    audio, sr = librosa.load(file, sr=None, mono=False)  # Load an audio file with librosa.
    args.sr = sr
    
    slicer = Slicer(args)
    chunks = slicer.slice(audio)
    
    input = input.replace("\\", "/")
    name = re.split("/", input)[-1].split(".")[0]
    print(f"name={name}")
    for i, chunk in enumerate(chunks):
        if len(chunk.shape) > 1:
            chunk = chunk.T  # Swap axes if the audio is stereo.
        soundfile.write(f'clips/{name}_{i}.wav', chunk, sr)  # Save sliced audio files with soundfile.
    