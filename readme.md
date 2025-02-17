# 🌧️🔥🐦 RainyBird [EN](./readme.md) / [中文](./readme_cn.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Everloom-129/RainyBird/blob/main/LICENSE)

Welcome to RainyBird! 🎵 Here is a small white noise mixer aimed at the soothing sounds of nature - from gentle forest whispers to cozy crackling fires. Using technology of digital signal processing(DSP) and Vision Language Models(VLMs), RainyBird helps you craft your own white noise for work, relaxation, or meditation.

## ✨ Features

- 🎚️ Create custom ambient white noise mixes that perfectly suit your mood
- 📊 Advanced Digital Signal Processing (DSP): Visualize and analyze sound waves
- 🔄 Seamlessly integrate multiple audio sources for rich, layered soundscapes
- 🤖 Get detailed quality assessment reports powered by advanced AI

## 📝 TODO List

- [ ] Beautiful Bird Calls
    - Winter Wren
      The Winter Wren is a small bird species, about 15cm in length and weighing around 20g. They typically inhabit northern coniferous forests and shrublands, feeding on insects, seeds, and berries. Their plumage is brown or gray with white underparts and tail. They produce sharp, loud calls, particularly during dawn and dusk. As migratory birds, they move to warmer regions during winter.
    - Hermit Thrush (Catharus guttatus)

    https://dongniao.net/nd/8730/%E9%9A%90%E5%A4%9C%E9%B8%AB/Hermit+Thrush/Hermit+Thrush

- [ ] Use AI voice synthesis (like ElevenLabs) to generate Dark Souls NPC-style voices
- [ ] Create "Morning Forest" themed images using AI image generation (like Midjourney)
- [ ] Add AI poetry recitation feature to the UI

## 🚀 Getting Started

### 📦 Prerequisites

```bash
pip install pydub librosa numpy scipy pillow openai matplotlib
```

### 🎮 Basic Usage

1. Generate White Noise Mix (3 minutes):
```bash
python scripts/analyze_mix.py sounds/birds-forest-morning.mp3 sounds/indoor-hard-rain-sound.mp3 sounds/fireplace-with-crackling-sounds.mp3
```

2. Add Optional Bird Calls:
```bash
python scripts/analyze_mix.py sounds/birds-forest-morning.mp3 sounds/indoor-hard-rain-sound.mp3 sounds/fireplace-with-crackling-sounds.mp3 voices/custom-bird-sound.mp3
```

3. Analyze Mix Quality:
```bash
# Real-time analysis (recommended)
python scripts/analyze_with_vlm.py results/mix_MMDD_HHMM

# Disable streaming output
python scripts/analyze_with_vlm.py results/mix_MMDD_HHMM --no-stream
```

## 📁 Project Structure

```
results/
  peaceful_forest_ambient_MMDD_HHMM/
    ├─ peaceful_forest_ambient_MMDD_HHMM.mp3  # Final mix
    ├─ vlm_feedback.md                        # Analysis report
    │
    ├─final_mix/                              # Final mix analysis
    │  ├─ *_analysis.png                      # Basic waveform analysis
    │  ├─ *_metadata.json                     # Audio metadata
    │  ├─ *_noise_analysis.json               # Noise analysis data
    │  └─ *_noise_analysis.png                # Detailed noise analysis
    │
    ├─forest/                                 # Forest sound analysis
    ├─rain/                                   # Rain sound analysis
    └─fire/                                   # Fire sound analysis
```

## 📊 Analysis Output

Each mix generates a comprehensive `vlm_feedback.md` file containing:
- 📝 Complete analysis report
- 📈 Technical metrics
- 🎵 Audio file information
- ⭐ Quality assessment

## 🎵 Resources

### Sound Sources

1. 🆓 Free sound tracks: [Pixabay Birds Sound Effects](https://pixabay.com/sound-effects/search/birds/)

2. 🦜 Bird call database:
    - Check out this amazing resource: [Xenopy Bird Data](https://github.com/realzza/xenopy/tree/birdData)
    - Download and upload bird calls for free!

3. 📜 The Road Not Taken: [Poetry Foundation](https://www.poetryfoundation.org/poems/44272/the-road-not-taken)

4. 🎮 Dark Souls Resources
    - Fire Keeper's Bedtime Stories: [YouTube Video](https://www.youtube.com/watch?v=THLh8SxRw-8&ab_channel=Firekeeper)
    - Bonfire Sound Effects: [Bonfire Dark Souls](https://www.myinstants.com/en/instant/bonfire-dark-souls-86656/)
    - Various short sound effects on My Instant: [My Instants Dark Souls](https://www.myinstants.com/en/search/?name=dark+souls)
    - Complete Dark Souls 3 NPC voice lines (800MB): [Reddit Post](https://www.reddit.com/r/opensouls3/comments/fm6pa3/all_dark_soul_3_npc_audio_files/)
    - Feel free to explore and customize these resources for your needs!

### 🔧 Technical References
- 📡 Signal Processing: Implements advanced DSP analysis tools from ECE310, ECE311 & ECE459
- 🤖 VLMs Analysis: Utilizes GPT-4V for sound quality assessment
- 🎚️ Audio Processing: Built with industry-standard audio processing libraries

## 🤝 Contributing

We'd love your contributions! Whether it's new sound samples, code improvements, or documentation updates - every contribution makes RainyBird better! Feel free to:
- 🔀 Submit a Pull Request
- 🐛 Open an Issue
- 💡 Share your ideas

## 📄 License

This project is open source and available under the MIT License. Feel free to use it in your own projects! 🎉

