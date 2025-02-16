from pydub import AudioSegment
from pydub.effects import normalize
import random
import datetime

# Configuration for volume parameters

TARGET_LEVEL = -20

BIRD_V  = -10  # Slightly reduce bird volume
WATER_V = -7  # Reduce water more (as background)
FIRE_V  = -20  # Fire as subtle background element
BIRD_CALL_V = -18  

def load_and_prepare_audio(file_path, target_volume=-20):
    """Load and normalize audio to consistent volume level"""
    print(f"Loading {file_path} ")
    audio = AudioSegment.from_file(file_path)
    return normalize(audio).apply_gain(target_volume - audio.dBFS)

def create_ambient_mix(bird_path, water_path, fire_path, duration_ms=180000):
    """
    Create peaceful ambient mix from bird sounds, water, and fire
    
    Parameters:
        bird_path: path to bird sounds file
        water_path: path to water sounds file
        fire_path: path to fire sounds file
        duration_ms: desired duration in milliseconds (default 3 minutes)
    """
    duration_ms = int(duration_ms)
    # Load and prepare audio files
    birds = load_and_prepare_audio(bird_path)
    water = load_and_prepare_audio(water_path)
    fire = load_and_prepare_audio(fire_path)
    
    # Normalize all sounds to same level first
    birds = birds.apply_gain(TARGET_LEVEL - birds.dBFS)
    water = water.apply_gain(TARGET_LEVEL - water.dBFS) 
    fire = fire.apply_gain(TARGET_LEVEL - fire.dBFS)

    # Adjust volumes for balance
    birds = birds + BIRD_V
    water = water + WATER_V
    fire  = fire  + FIRE_V
    
    # Loop tracks if they're shorter than desired duration
    birds = birds * (duration_ms // len(birds) + 1)
    water = water * (duration_ms // len(water) + 1)
    fire = fire * (duration_ms // len(fire) + 1)
    
    # Trim to exact duration
    birds = birds[:duration_ms]
    water = water[:duration_ms]
    fire = fire[:duration_ms]
    
    # Add subtle fade in/out
    fade_duration = 3000  # 3 seconds
    birds = birds.fade_in(fade_duration).fade_out(fade_duration)
    # water = water.fade_in(fade_duration).fade_out(fade_duration)
    fire = fire.fade_in(fade_duration).fade_out(fade_duration)
    
    # Overlay all tracks
    final_mix = birds.overlay(water)
    final_mix = final_mix.overlay(fire)
    
    # Final normalization and export
    final_mix = normalize(final_mix)
    return final_mix


def add_timed_bird_calls(base_mix, bird_calls_path, interval_ms=30000, call_duration_ms=5000):
    """
    Add bird calls at regular intervals with smooth fade in/out
    
    Parameters:
        base_mix: The base ambient mix
        bird_calls_path: Path to bird call sound file
        interval_ms: Time between calls in milliseconds (default 30s)
        call_duration_ms: Duration of each call in milliseconds (default 5s)
    """
    if not bird_calls_path:
        return base_mix
        
    result = base_mix
    bird_call = load_and_prepare_audio(bird_calls_path)
    
    if len(bird_call) > call_duration_ms:
        bird_call = bird_call[:call_duration_ms]
 
    
    # Add fade in/out for smoothness
    fade_ms = 500  # 0.5 second fade
    bird_call = bird_call.fade_in(fade_ms).fade_out(fade_ms)
    
    bird_call = bird_call.apply_gain(TARGET_LEVEL - bird_call.dBFS)
    bird_call = bird_call - BIRD_CALL_V  # Adjust this value as needed
    
    # Calculate number of intervals that fit in the base mix
    total_duration = len(base_mix)
    num_intervals = total_duration // interval_ms
    
    # Add calls at regular intervals, with slight random timing variation
    for i in range(num_intervals):
        # Add some randomness to the timing (±2 seconds)
        random_offset = random.randint(-2000, 2000)
        position = (i * interval_ms) + random_offset
        
        # Ensure position is within bounds
        if position < 0:
            position = 0
        if position + len(bird_call) > len(base_mix):
            continue
            
        result = result.overlay(bird_call, position=position)
    
    return result

def add_intro_outro(base_mix: AudioSegment, 
                   intro_sound: str = None,
                   outro_sound: str = None,
                   crossfade_ms: int = 4000) -> AudioSegment:
    """Add intro and/or outro sounds to the base mix with smooth transitions.
    
    Parameters:
        base_mix: The base ambient mix
        intro_sound: Path to intro sound file (optional)
        outro_sound: Path to outro sound file (optional)
        crossfade_ms: Duration of crossfade in milliseconds (default 4s)
        
    Returns:
        AudioSegment with added intro/outro
    """
    result = base_mix
    
    if intro_sound:
        intro = load_and_prepare_audio(intro_sound)
        intro = intro.apply_gain(base_mix.dBFS - intro.dBFS)
        result = intro.append(base_mix, crossfade=crossfade_ms)
    
    if outro_sound:
        outro = load_and_prepare_audio(outro_sound)
        outro = outro.apply_gain(base_mix.dBFS - outro.dBFS)
        result = result.append(outro, crossfade=crossfade_ms)
    
    return result

if __name__ == "__main__":
    # Get input paths from command line arguments
    import sys
    import datetime
    import random
    
    if len(sys.argv) < 4:
        print("Usage: python sound_mixer.py <forest_sound> <rain_sound> <fire_sound> [bird_call_sound] [intro_sound] [outro_sound]")
        print("Example: python sound_mixer.py sounds/birds-forest-morning.mp3 sounds/indoor-hard-rain-sound.mp3 sounds/fireplace-with-crackling-sounds.mp3")
        sys.exit(1)
        
    forest_sound = sys.argv[1]
    rain_sound = sys.argv[2]
    fire_sound = sys.argv[3]
    bird_call_sound = sys.argv[4] if len(sys.argv) > 4 else None
    intro_sound = sys.argv[5] if len(sys.argv) > 5 else None
    outro_sound = sys.argv[6] if len(sys.argv) > 6 else None
    
    # Create base mix
    ambient_mix = create_ambient_mix(
        forest_sound,
        rain_sound, 
        fire_sound,
        duration_ms=60000 * 5 # 5 minutes
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
    
    # Export the final mix
    result_mix_path = f"results/mix_{datetime.datetime.now().strftime('%m%d_%H%M')}.mp3"
    final_mix.export(result_mix_path, format="mp3", bitrate="320k")
    print(f"Finish mixing, result is stored in {result_mix_path}")