import librosa
import noisereduce as nr
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import soundfile as sf
import os

# Load audio
def load_audio(input_path: str):
    if input_path.endswith('.mp3'):
        audio = AudioSegment.from_mp3(input_path)
        wav_path = input_path.replace('.mp3', '.wav')
        audio.export(wav_path, format='wav')
        data, sr = librosa.load(wav_path, sr=None, mono=True)
        os.remove(wav_path)
    else:
        data, sr = librosa.load(input_path, sr=None, mono=True)
    return data, sr

# Save audio
def save_audio(data: np.ndarray, sr: int, output_path: str):
    temp_path = "data/temp/temp_processed.wav"
    sf.write(temp_path, data, sr)
    audio = AudioSegment.from_wav(temp_path)
    audio.export(output_path, format="wav")
    os.remove(temp_path)


## Audio processing
# Spectral noise reduction
def reduce_noise(input_path: str, output_path: str, reduction_strength=0.5):
    data, sr = load_audio(input_path)
    reduced_noise = nr.reduce_noise(
        y=data, 
        sr=sr,
        prop_decrease=reduction_strength
    )
    save_audio(reduced_noise, sr, output_path)

# Bandpass filter
def apply_bandpass_filter(input_path: str, output_path: str, lowcut=300, highcut=3400):
    data, sr = load_audio(input_path)
    
    def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    b, a = butter_bandpass(lowcut, highcut, sr)
    filtered = filtfilt(b, a, data)
    save_audio(filtered, sr, output_path)

# Volume normalization
def normalize_volume(input_path: str, output_path: str, target_dBFS=-20.0):
    data, sr = load_audio(input_path)
    temp_path = "data/temp/temp_normalize.wav"
    sf.write(temp_path, data, sr)
    
    audio = AudioSegment.from_wav(temp_path)
    change_in_dBFS = target_dBFS - audio.dBFS
    normalized = audio.apply_gain(change_in_dBFS)
    normalized.export(output_path, format="wav")
    os.remove(temp_path)