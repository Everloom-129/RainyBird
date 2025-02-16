# Rainy Mood + Bird Call Background Music

#!/bin/bash

# Set paths to sound files
FOREST_SOUND="voices/我好想你-苏打绿.mp3"

# FOREST_SOUND="voices/The-Road-Not-Taken.m4a"
# FOREST_SOUND="sounds/Touch-the-Rain-Jannik.flac"
RAIN_SOUND="sounds/RainyMood-34min.mp3" 
FIRE_SOUND="sounds/fireplace-with-crackling-sounds.mp3"
BIRD_CALL="voices/canada-goose-honks.mp3"

OUTPUT_NAME="sodagreen-rainy-bird"
DURATION=400000

# Call the sound mixer script
python scripts/analyze_mix.py "$FOREST_SOUND" "$RAIN_SOUND" "$FIRE_SOUND" "$BIRD_CALL" "$DURATION" "$OUTPUT_NAME"

# python scripts/analyze_with_vlm.py "results/$OUTPUT_NAME"
