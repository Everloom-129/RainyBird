import numpy as np
import matplotlib.pyplot as plt
from pydub.utils import get_array_type
import array
import librosa
import librosa.display

def plot_waveform(audio_segment, title="Waveform"):
    # Extract raw samples as a numpy array
    samples = np.array(audio_segment.get_array_of_samples())
    plt.figure(figsize=(12, 4))
    plt.plot(samples, color='navy')
    plt.title(title)
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

def plot_spectrogram(audio_segment, title="Spectrogram"):
    # Convert pydub AudioSegment to numpy array and get sample rate
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    sr = audio_segment.frame_rate
    # Normalize samples to [-1,1]
    samples = samples / (2**15)
    
    # Compute the Mel spectrogram
    S = librosa.feature.melspectrogram(y=samples, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Example usage after you generate final_mix:
# plot_waveform(final_mix, "Final Mix Waveform")
# plot_spectrogram(final_mix, "Final Mix Spectrogram")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_spectrogram.py <audio_file>")
        sys.exit(1)
        
    audio_file = sys.argv[1]
    from pydub import AudioSegment
    audio = AudioSegment.from_file(audio_file)
    plot_waveform(audio, f"Waveform - {audio_file}")
    plot_spectrogram(audio, f"Spectrogram - {audio_file}")