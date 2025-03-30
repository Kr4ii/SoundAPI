import librosa
import noisereduce as nr
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import soundfile as sf
import os

def process_audio(input_path: str, output_path: str):
    try:
        # Load audio
        if input_path.endswith('.mp3'):
            audio = AudioSegment.from_mp3(input_path)
            wav_path = input_path.replace('.mp3', '.wav')
            audio.export(wav_path, format='wav')
            data, sr = librosa.load(wav_path, sr=None, mono=True)
            os.remove(wav_path)
        else:
            data, sr = librosa.load(input_path, sr=None, mono=True)

        # Spectral noise reduction
        reduced_noise = nr.reduce_noise(y=data, sr=sr)

        # Bandpass filter
        def butter_bandpass(lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs # Nyqist freq
            low = lowcut / nyq
            high = highcut / nyq
            b, a = butter(order, [low, high], btype='band')
            return b, a

        b, a = butter_bandpass(300, 3400, sr)
        filtered = filtfilt(b, a, reduced_noise)

        # Normalization
        temp_path = "data/temp/temp_filtered.wav"
        sf.write(temp_path, filtered, sr)
        audio = AudioSegment.from_wav(temp_path)
        normalized = audio.normalize()
        normalized.export(output_path, format="wav")
        os.remove(temp_path)

    except Exception as e:
        raise e