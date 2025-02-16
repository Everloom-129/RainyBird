import numpy as np
from scipy import signal
from scipy import stats
import librosa
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Optional
import json

# Digital Signal Processing 
# FSD analysis from ECE459: Communications Systems
# Tony Wang - 2025-02-13 V1
# 

class SignalAnalyzer:
    def __init__(self):
        """Initialize the signal analyzer with default parameters"""
        self.sample_rate = None
        self.samples = None
        
    def load_samples(self, samples: np.ndarray, sample_rate: int):
        """Load audio samples and sample rate for analysis"""
        self.samples = samples
        self.sample_rate = sample_rate
        
    def compute_psd(self, segment_length: int = 2048, overlap: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
        """Compute Power Spectral Density using Welch's method.
        
        Args:
            segment_length: Length of each segment for Welch's method
            overlap: Overlap between segments (0 to 1)
            
        Returns:
            Tuple of (frequencies, psd)
        """
        frequencies, psd = signal.welch(
            self.samples,
            self.sample_rate,
            nperseg=segment_length,
            noverlap=int(segment_length * overlap)
        )
        return frequencies, psd
    
    def compute_autocorrelation(self, max_lag: Optional[int] = None) -> np.ndarray:
        """Compute autocorrelation function.
        
        Args:
            max_lag: Maximum lag to compute (default: len(samples)//2)
            
        Returns:
            Autocorrelation values
        """
        if max_lag is None:
            max_lag = len(self.samples) // 2
            
        autocorr = signal.correlate(self.samples, self.samples, mode='full')
        # Keep only positive lags and normalize
        autocorr = autocorr[len(autocorr)//2:len(autocorr)//2 + max_lag]
        return autocorr / autocorr[0]
    
    def compute_spectral_flatness(self, n_fft: int = 2048) -> float:
        """Compute spectral flatness (Wiener entropy).
        
        Args:
            n_fft: FFT window size
            
        Returns:
            Spectral flatness value (0 to 1)
        """
        spectrum = np.abs(librosa.stft(self.samples, n_fft=n_fft))
        power_spectrum = np.square(spectrum)
        
        # Compute geometric and arithmetic means
        geometric_mean = np.exp(np.mean(np.log(power_spectrum + 1e-10), axis=0))
        arithmetic_mean = np.mean(power_spectrum, axis=0)
        
        # Compute flatness and average over time
        flatness = geometric_mean / (arithmetic_mean + 1e-10)
        return float(np.mean(flatness))
    
    def analyze_distribution(self) -> Dict:
        """Analyze the statistical distribution of the samples.
        
        Returns:
            Dictionary containing distribution statistics and test results
        """
        # Compute basic statistics
        mean = np.mean(self.samples)
        std = np.std(self.samples)
        skewness = stats.skew(self.samples)
        kurtosis = stats.kurtosis(self.samples)
        
        # Perform Kolmogorov-Smirnov test for normality
        ks_statistic, ks_pvalue = stats.kstest(
            (self.samples - mean) / std,  # Normalize samples
            'norm'  # Test against normal distribution
        )
        
        return {
            "mean": float(mean),
            "std": float(std),
            "skewness": float(skewness),
            "kurtosis": float(kurtosis),
            "ks_test": {
                "statistic": float(ks_statistic),
                "p_value": float(ks_pvalue)
            }
        }
    
    def plot_noise_analysis(self, output_path: str):
        """Generate comprehensive noise analysis plots.
        
        Args:
            output_path: Path to save the plot
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Power Spectral Density
        freqs, psd = self.compute_psd()
        ax1.semilogy(freqs, psd)
        ax1.set_title('Power Spectral Density')
        ax1.set_xlabel('Frequency [Hz]')
        ax1.set_ylabel('PSD [V**2/Hz]')
        ax1.grid(True)
        
        # Plot 2: Autocorrelation
        lags = np.arange(1000)  # Show first 1000 lags
        autocorr = self.compute_autocorrelation(max_lag=1000)
        ax2.plot(lags, autocorr)
        ax2.set_title('Autocorrelation Function')
        ax2.set_xlabel('Lag')
        ax2.set_ylabel('Correlation')
        ax2.grid(True)
        
        # Plot 3: Sample Distribution
        ax3.hist(self.samples, bins=100, density=True, alpha=0.7)
        xmin, xmax = ax3.get_xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, np.mean(self.samples), np.std(self.samples))
        ax3.plot(x, p, 'k', linewidth=2)
        ax3.set_title('Sample Distribution')
        ax3.set_xlabel('Amplitude')
        ax3.set_ylabel('Density')
        ax3.grid(True)
        
        # Plot 4: STFT Spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.samples)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='linear', x_axis='time', ax=ax4)
        fig.colorbar(img, ax=ax4, format='%+2.0f dB')
        ax4.set_title('Spectrogram')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def analyze_noise(self, output_path_prefix: str) -> Dict:
        """Perform comprehensive noise analysis and save results.
        
        Args:
            output_path_prefix: Prefix for output files (without extension)
            
        Returns:
            Dictionary containing all analysis results
        """
        # Compute all metrics
        spectral_flatness = self.compute_spectral_flatness()
        distribution_stats = self.analyze_distribution()
        
        # Generate plots
        plot_path = f"{output_path_prefix}_noise_analysis.png"
        self.plot_noise_analysis(plot_path)
        
        # Compile results
        results = {
            "spectral_flatness": spectral_flatness,
            "distribution_analysis": distribution_stats,
            "noise_analysis_plot": plot_path
        }
        
        # Save results to JSON
        json_path = f"{output_path_prefix}_noise_analysis.json"
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=4)
            
        return results 