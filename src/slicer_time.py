from pydub import AudioSegment
from pydub.utils import make_chunks
import re

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
    cuts = make_chunks(audio, size)  #将文件切割为10s一块
    print(f"====chunks={cuts}")
    for i, seg in enumerate(cuts):
        chunk = seg.raw_data
        if chunk is None or "shape" not in chunk or len(chunk) < 1 :
            continue
        #chunk_name = "chunk{0}.wav".format(i)
        print ("exporting", i, seg.raw_data.shape)
        #chunk.export(chunk_name, format="wav")
        chunks.append(seg.raw_data)
    return chunks