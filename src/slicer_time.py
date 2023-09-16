from pydub import AudioSegment
from pydub.utils import make_chunks
import re
import numpy as np
import librosa
import match
# 按时间切换, 默认20s
def slicer_time(y: np.array, sr:int, time_unit:int=20000):
    duration = librosa.get_duration(y=audio, sr=sr)
    count = match.ceil(duration *1000 /time_unit)
    chunks = []
    for i in range(count):
        chunks.append()
        
    return chunks
    
def pydub_to_np(audio: AudioSegment) -> (np.ndarray, int):
    """
    Converts pydub audio segment into np.float32 of shape [duration_in_seconds*sample_rate, channels],
    where each value is in range [-1.0, 1.0]. 
    Returns tuple (audio_np_array, sample_rate).
    """
    return np.array(audio.get_array_of_samples(), dtype=np.float32).reshape((-1, audio.channels)) / (
            1 << (8 * audio.sample_width - 1)), audio.frame_rate