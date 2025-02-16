import os
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import librosa
import librosa.display
from datetime import datetime
from typing import Optional, Tuple, Dict
import json
from signal_analysis import SignalAnalyzer

class AudioAnalysisPipeline:
    def __init__(self, output_base_dir: str = "results"):
        """Initialize the audio analysis pipeline.
        
        Args:
            output_base_dir: Base directory for saving results
        """
        self.output_base_dir = output_base_dir
        self.signal_analyzer = SignalAnalyzer()
        
    def create_output_directory(self, name: Optional[str] = None) -> str:
        """Create and return the output directory path."""
        if name is None:
            name = datetime.now().strftime("%m%d_%H%M")
        
        output_dir = os.path.join(self.output_base_dir, name)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
        
    def analyze_audio(self, audio_path: str, name: Optional[str] = None) -> Dict:
        """Analyze audio file and generate visualizations.
        
        Args:
            audio_path: Path to the audio file
            name: Optional name for the output directory
            
        Returns:
            Dictionary containing analysis results and paths
        """
        # Load audio
        audio = AudioSegment.from_file(audio_path)
        
        # Create output directory
        output_dir = self.create_output_directory(name)
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot waveform
        samples = np.array(audio.get_array_of_samples())
        ax1.plot(samples, color='navy')
        ax1.set_title("Waveform")
        ax1.set_xlabel("Samples")
        ax1.set_ylabel("Amplitude")
        
        # Plot spectrogram
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        sr = audio.frame_rate
        samples = samples / (2**15)  # Normalize
        
        # Perform signal analysis
        self.signal_analyzer.load_samples(samples, sr)
        noise_analysis = self.signal_analyzer.analyze_noise(
            os.path.join(output_dir, base_name)
        )
        
        S = librosa.feature.melspectrogram(y=samples, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        img = librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', 
                                     cmap='magma', ax=ax2)
        fig.colorbar(img, ax=ax2, format='%+2.0f dB')
        ax2.set_title("Mel Spectrogram")
        
        # Adjust layout and save
        plt.tight_layout()
        
        # Save visualization
        viz_path = os.path.join(output_dir, f"{base_name}_analysis.png")
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Calculate audio statistics
        duration = len(audio) / 1000.0  # in seconds
        channels = audio.channels
        sample_width = audio.sample_width
        frame_rate = audio.frame_rate
        
        # Save metadata
        metadata = {
            "filename": os.path.basename(audio_path),
            "duration": duration,
            "channels": channels,
            "sample_width": sample_width,
            "frame_rate": frame_rate,
            "visualization_path": viz_path,
            "noise_analysis": noise_analysis  # Add noise analysis results
        }
        
        metadata_path = os.path.join(output_dir, f"{base_name}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
            
        return metadata
        
    def analyze_mix_components(self, 
                             components: Dict[str, str],
                             output_name: Optional[str] = None) -> Dict:
        """Analyze multiple audio components and their mix.
        
        Args:
            components: Dictionary mapping component names to file paths
            output_name: Optional name for the output directory
            
        Returns:
            Dictionary containing analysis results for all components
        """
        if output_name is None:
            output_name = f"mix_analysis_{datetime.now().strftime('%m%d_%H%M')}"
            
        results = {}
        for name, path in components.items():
            results[name] = self.analyze_audio(path, f"{output_name}/{name}")
            
        return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_pipeline.py <audio_file>")
        sys.exit(1)
        
    pipeline = AudioAnalysisPipeline()
    results = pipeline.analyze_audio(sys.argv[1])
    print(f"Analysis complete. Results saved to: {results['visualization_path']}") 