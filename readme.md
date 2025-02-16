# RainyBird

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Everloom-129/RainyBird/blob/main/LICENSE)

RainyBird is an advanced audio processing tool that creates immersive ambient soundscapes by combining natural sounds like forest ambiance, rainfall, and crackling fires. It features sophisticated audio mixing capabilities and AI-powered sound quality analysis.

## Features

- [x] Create custom ambient white noise mixes
- [x] Digital Signal Processing (DSP): sound wave and noise analysis visualization
- [x] Multiple audio source integration
- [x] VLMs based quality assessment reports



✅ **录制一个黑魂风格的篝火旁对白**

✅ **自己写一小段"旅人独白"**，然后录音，加上篝火燃烧的背景音

✅ **观鸟+冥想声音**

✅ 录一段**"晨间森林"**的声音，把鸟叫、流水、篝火燃烧的声音合成一个**白噪音**



## TODO 

- [ ] 好听的鸟叫
    - winter wren
    冬鸫，也叫雪鸫，是一种小型鸟类，体长约15厘米，体重约20克。它们通常生活在北方的针叶林和灌木丛中，以昆虫、种子和浆果为食。冬鸫的羽毛呈棕色或灰色，带有白色的腹部和尾巴。它们的叫声尖锐而响亮，常常在清晨和傍晚时分鸣叫。冬鸫是候鸟，冬季会迁徙到温暖的地区过冬。
    - 隐夜鸫 Hermit Thrush Catharus guttatus

    https://dongniao.net/nd/8730/%E9%9A%90%E5%A4%9C%E9%B8%AB/Hermit+Thrush/Hermit+Thrush

- [ ] 可以用 **AI 语音合成**，比如 ElevenLabs 来生成黑魂 NPC 风格的声音
- [ ] 用 **AI 图片生成**，比如 Midjourney 来生成一个关于"晨间森林"的图片
- [ ] 增加AI 诗朗诵？可以集成到UI里


## Getting Started

### Prerequisites

```bash
pip install pydub librosa numpy scipy pillow openai matplotlib
```

### Basic Usage

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

## Project Structure

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

## Analysis Output

Each mix generates a comprehensive `vlm_feedback.md` file containing:
- Complete analysis report
- Technical metrics
- Audio file information
- Quality assessment

## Resources

### Sound Sources

1. Free sound track: [Pixabay Birds Sound Effects](https://pixabay.com/sound-effects/search/birds/)

2. Bird call database / 鸟叫声：
    - 发现了一个很厉害的网站：[Xenopy Bird Data](https://github.com/realzza/xenopy/tree/birdData)
    - 里面有各种鸟的叫声，可以用来做背景音, 可以自行上传，免费下载
    - 我上传了棕头鸦雀的叫声，效果还不错

3. 棕头鸦雀 / Vinous-throated parrotbill：
    - 太难找了，使用了b站的视频：[Bilibili Video](https://www.bilibili.com/video/BV1Fr421W7kE/)
    - 用这个浏览器插件录制了视频的音频，效果不错：chrome-extension@Chrome Audio Capture

4. The Road Not Taken: [Poetry Foundation](https://www.poetryfoundation.org/poems/44272/the-road-not-taken)

5. 黑魂相关的
    - 伟大的防火女妈妈，睡前故事：[YouTube Video](https://www.youtube.com/watch?v=THLh8SxRw-8&ab_channel=Firekeeper)
    - Bon fire track: [Bonfire Dark Souls](https://www.myinstants.com/en/instant/bonfire-dark-souls-86656/)
    - my instant有很多音源，不过比较短：[My Instants Dark Souls](https://www.myinstants.com/en/search/?name=dark+souls)
    - 有人hack了黑魂的soundtrack，这里是800mb所有角色的语音条：[Reddit Post](https://www.reddit.com/r/opensouls3/comments/fm6pa3/all_dark_soul_3_npc_audio_files/)
    - 太多了暂时就没筛选，有兴趣的可以自己调试一下
    - [ ] 增加AI诗朗诵？可以集成到UI里



### Technical References
- Signal Processing: Implements advanced DSP analysis tools from ECE310, ECE311 & ECE459
- VLMs Analysis: Utilizes GPT-4V for sound quality assessment from [OpenAI](https://platform.openai.com/docs/models/gpt-4o-latest)
- Audio Processing: Built with industry-standard audio processing libraries

## Contributing
欢迎各位鸟友、雨声爱好者、黑魂爱好者的贡献！

我们特别欢迎以下方面的贡献：
- 新的鸟类音频资源
- 高质量的雨声、森林环境音效
- 黑魂系列相关的音频素材
- 代码改进和功能增强
- Bug修复和性能优化
- 文档完善和翻译工作

您可以通过以下方式参与：
- 提交Pull Request
- 创建Issue反馈问题
- 分享宝贵的建议和想法

Contributions are welcome! Please feel free to submit pull requests, open issues, or suggest improvements.

## License

This project is open source and available under the MIT License.

