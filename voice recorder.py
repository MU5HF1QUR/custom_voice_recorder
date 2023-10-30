import os
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import wave

# Create folders if they don't exist
audio_folder = "recordings"
os.makedirs(audio_folder, exist_ok=True)

spectrogram_folder = "spectrograms"
os.makedirs(spectrogram_folder, exist_ok=True)

FORMAT = pyaudio.paInt16  # Format of audio samples (16-bit signed integers)
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100              # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 5        # Duration of recording in seconds

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

stream.stop_stream()
stream.close()

p.terminate()

# Convert the recorded frames to a NumPy array
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

# Generate a unique filename based on the current timestamp
import random
num = int(random.randrange(0, 500000, 3))
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
audio_filename = os.path.join(audio_folder, f"recorded_audio_{timestamp}_{num}.wav")
spectrogram_filename = os.path.join(spectrogram_folder, f"spectrogram_{timestamp}_{num}.png")

# Save the recorded audio
with wave.open(audio_filename, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Create a spectrogram and save it as an image
plt.specgram(audio_data, Fs=RATE, cmap='viridis')
plt.axis('off')  # Turn off axes for cleaner image
plt.savefig(spectrogram_filename, bbox_inches='tight', pad_inches=0, transparent=True)
plt.close()

print(f"Recorded audio saved as {audio_filename}")
print(f"Spectrogram saved as {spectrogram_filename}")
