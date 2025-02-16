# Rainy Mood + Bird Call Background Music

#!/bin/bash

# Set paths to sound files
FOREST_SOUND="sounds/birds-forest-morning.mp3"
RAIN_SOUND="sounds/indoor-hard-rain-sound.mp3" 
FIRE_SOUND="sounds/fireplace-with-crackling-sounds.mp3"
BIRD_CALL="voices/Vinous-throated-parrotbill-call.mp3"

# Call the sound mixer script
python scripts/analyze_mix.py "$FOREST_SOUND" "$RAIN_SOUND" "$FIRE_SOUND" "$BIRD_CALL"

