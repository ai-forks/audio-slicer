from pydub import AudioSegment
from pydub.utils import make_chunks
import re
import numpy as np
# 按时间切换, 默认20s
def slicer_time(file: str, time_unit:int=20000):
    file = file.replace("\\", "/")
    names = ext = re.split("/", file)[-1]
    name = names.split(".")[0]
    ext = names.split(".")[1]
    ext = ext if ext is not None and len(ext) > 0 else "wav"
    print(f"slicer_time file={file} ext={ext}")
    audio = AudioSegment.from_file(file, ext)
    size = time_unit   #切割的毫秒数 10s=10000
    chunks = []
    segs = make_chunks(audio, size)  #将文件切割为10s一块
    print(f"====chunks={segs}")
    for i, seg in enumerate(segs):
        chunk = pydub_to_np(seg)
        #chunk_name = "chunk{0}.wav".format(i)
        print ("exporting", i, seg.channels)
        #chunk.export(chunk_name, format="wav")
        chunks.append(chunk)
    print(f"outreoult = {chunks}")
    return chunks
    
def pydub_to_np(audio: AudioSegment) -> (np.ndarray, int):
    """
    Converts pydub audio segment into np.float32 of shape [duration_in_seconds*sample_rate, channels],
    where each value is in range [-1.0, 1.0]. 
    Returns tuple (audio_np_array, sample_rate).
    """
    return np.array(audio.get_array_of_samples(), dtype=np.float32).reshape((-1, audio.channels)) / (
            1 << (8 * audio.sample_width - 1)), audio.frame_rate