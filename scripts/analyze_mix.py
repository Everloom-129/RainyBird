import os
from sound_mixer import create_ambient_mix, add_timed_bird_calls, add_intro_outro
from audio_pipeline import AudioAnalysisPipeline
from datetime import datetime

def analyze_mix_with_components(
    forest_sound: str,
    rain_sound: str,
    fire_sound: str,
    bird_call_sound: str = None,
    duration_ms: int = 300000,  # 5 minutes
    output_name: str = None,
    intro_sound: str = None,
    outro_sound: str = None
) -> dict:
    """Create an ambient mix and analyze all components including the final mix.
    
    Args:
        forest_sound: Path to forest ambient sound file
        rain_sound: Path to rain sound file
        fire_sound: Path to fire sound file
        bird_call_sound: Optional path to bird call sound file
        intro_sound: Optional path to intro sound file
        outro_sound: Optional path to outro sound file
        duration_ms: Duration of the mix in milliseconds
        output_name: Optional name for the output directory
        
    Returns:
        Dictionary containing analysis results for all components and final mix
    """
    if output_name is None:
        output_name = f"mix_{datetime.now().strftime('%m%d_%H%M')}"
        
    # Create the mix
    ambient_mix = create_ambient_mix(
        forest_sound,
        rain_sound,
        fire_sound,
        duration_ms=duration_ms
    )
    
    # Add bird calls if provided
    if bird_call_sound:
        ambient_mix = add_timed_bird_calls(
            ambient_mix,
            bird_call_sound,
            interval_ms=30000,  # Call every 30 seconds
            call_duration_ms=5000  # Each call lasts 5 seconds
        )
    
    # Add intro/outro if provided
    final_mix = add_intro_outro(
        ambient_mix,
        intro_sound=intro_sound,
        outro_sound=outro_sound
    )
    
    # Export the mix
    os.makedirs("results", exist_ok=True)
    mix_path = f"results/{output_name}/{output_name}.mp3"
    os.makedirs(os.path.dirname(mix_path), exist_ok=True)
    final_mix.export(mix_path, format="mp3", bitrate="320k")
    
    # Initialize pipeline
    pipeline = AudioAnalysisPipeline()
    
    # Analyze all components
    components = {
        "forest": forest_sound,
        "rain": rain_sound,
        "fire": fire_sound,
        "final_mix": mix_path
    }
    
    if bird_call_sound:
        components["bird_calls"] = bird_call_sound
    if intro_sound:
        components["intro"] = intro_sound
    if outro_sound:
        components["outro"] = outro_sound
        
    # Run analysis
    results = pipeline.analyze_mix_components(components, output_name)
    
    # Print noise analysis summary
    print(f"\nAnalysis complete! Results saved to results/{output_name}/")
    print(f"Final mix saved as: {mix_path}")
    print("\nNoise Analysis Summary:")
    print("-" * 50)
    
    for component, result in results.items():
        noise_analysis = result.get("noise_analysis", {})
        spectral_flatness = noise_analysis.get("spectral_flatness", 0)
        distribution = noise_analysis.get("distribution_analysis", {})
        
        print(f"\n{component.upper()}:")
        print(f"  Spectral Flatness: {spectral_flatness:.4f}")
        print(f"  Distribution Statistics:")
        print(f"    Mean: {distribution.get('mean', 0):.4f}")
        print(f"    Std Dev: {distribution.get('std', 0):.4f}")
        print(f"    Skewness: {distribution.get('skewness', 0):.4f}")
        print(f"    Kurtosis: {distribution.get('kurtosis', 0):.4f}")
        
        ks_test = distribution.get("ks_test", {})
        print(f"  Normality Test (K-S):")
        print(f"    Statistic: {ks_test.get('statistic', 0):.4f}")
        print(f"    P-value: {ks_test.get('p_value', 0):.4f}")
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python analyze_mix.py <forest_sound> <rain_sound> <fire_sound> [bird_call_sound] [intro_sound] [outro_sound]")
        print("Example: python analyze_mix.py sounds/birds-forest-morning.mp3 sounds/indoor-hard-rain-sound.mp3 sounds/fireplace-with-crackling-sounds.mp3")
        sys.exit(1)
        
    forest_sound = sys.argv[1]
    rain_sound = sys.argv[2]
    fire_sound = sys.argv[3]
    bird_call_sound = sys.argv[4] if len(sys.argv) > 4 else None
    duration_ms = sys.argv[5] if len(sys.argv) > 5 else 300000
    output_name = sys.argv[6] if len(sys.argv) > 6 else f"mix_{datetime.now().strftime('%m%d_%H%M')}"
    intro_sound = sys.argv[7] if len(sys.argv) > 7 else None
    outro_sound = sys.argv[8] if len(sys.argv) > 8 else None
    
    results = analyze_mix_with_components(
        forest_sound,
        rain_sound,
        fire_sound,
        bird_call_sound,
        duration_ms=duration_ms,
        output_name=output_name,
        intro_sound=intro_sound,
        outro_sound=outro_sound
    )