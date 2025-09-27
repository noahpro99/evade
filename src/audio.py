import numpy as np
import pyaudio
import whisper


def transcribe_audio():
    # start thread for audio transcription
    model = whisper.load_model("small")  # Changed to "small" for better accuracy

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4096,
    )

    print("Listening...")
    buffer = []
    buffer_duration = 5  # seconds
    samples_per_second = 16000
    frames_needed = int(samples_per_second * buffer_duration / 4096)  # Approximate

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        buffer.append(data)

        if len(buffer) >= frames_needed:
            # Concatenate buffer
            full_data = b"".join(buffer)
            audio = np.frombuffer(full_data, np.int16).astype(np.float32) / 32768.0
            result = model.transcribe(audio, fp16=False)
            print(result["text"])
            buffer = []  # Clear buffer


if __name__ == "__main__":
    transcribe_audio()
