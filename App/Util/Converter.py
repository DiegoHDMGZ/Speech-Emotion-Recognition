import io
from pydub import AudioSegment
import torchaudio


def convert(audio_bytes):
    audio = io.BytesIO(audio_bytes)
    fileformat = "wav"
    filename = "test.wav"
    AudioSegment.from_file(audio).export(filename, format=fileformat)
    return torchaudio.load(filename)

