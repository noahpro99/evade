import numpy as np
import pyaudio
import whisper


def transcribe_audio():
    # start thread for audio transcription
    model = whisper.load_model("base")

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4096,
    )

    print("Listening...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        audio = np.frombuffer(data, np.int16).astype(np.float32) / 32768.0
        result = model.transcribe(audio, fp16=False)
        print(result["text"])


if __name__ == "__main__":
    transcribe_audio()
