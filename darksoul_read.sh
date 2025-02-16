# Dark Souls BGM / Soundtrack

#!/bin/bash

# Set paths to sound files
FOREST_SOUND="voices/firekeeper-reads-to-you-at-night.mp3"
RAIN_SOUND="sounds/RainyMood-34min.mp3" 
FIRE_SOUND="sounds/fireplace-with-crackling-sounds.mp3"
BIRD_CALL="sounds/darksoul_bonfire_jump.mp3"
INTRO="voices/ashen-one.mp3"
OUTRO="sounds/you-died-dark-souls.mp3"
DURATION=900000
OUTPUT_NAME="Firekeeper-reads-to-you-at-night"

python scripts/analyze_mix.py "$FOREST_SOUND" "$RAIN_SOUND" "$FIRE_SOUND" "$BIRD_CALL" "$DURATION" "$OUTPUT_NAME"  "$INTRO" "$OUTRO"
# Feedback from VLM

python scripts/analyze_with_vlm.py "results/$OUTPUT_NAME"
