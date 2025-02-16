# SHIT - Rando
# https://www.reddit.com/r/shittydarksouls/
# https://darksouls.fandom.com/wiki/Dung_Pie

# 屎
# Atrocious fecal waste material. Throw at enemy to build up toxins,
# but also builds up your toxicity,
# Although the stench makes it difficult to carry on one's person, 
# turning an enemy toxic inflicts high damage over a period of time.

#!/bin/bash

# Set paths to sound files
FOREST_SOUND="sounds/dark-souls-kill.mp3"
RAIN_SOUND="sounds/RainyMood-34min.mp3" 
FIRE_SOUND="sounds/fireplace-with-crackling-sounds.mp3"
BIRD_CALL="sounds/you-died-dark-souls.mp3"
INTRO="sounds/darksoul_bonfire_jump.mp3"
OUTRO="sounds/you-died-dark-souls.mp3"
DURATION=100000
OUTPUT_NAME="dung-pie"

python scripts/analyze_mix.py "$FOREST_SOUND" "$RAIN_SOUND" "$FIRE_SOUND" "$BIRD_CALL" "$DURATION" "$OUTPUT_NAME" "$INTRO" "$OUTRO"
