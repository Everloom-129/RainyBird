# 🌧️🔥🐦 RainyBird [EN](./readme.md) / [中文](./readme_cn.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Everloom-129/RainyBird/blob/main/LICENSE)

RainyBird 是一个简洁开源的音频处理工具，通过组合森林环境音、雨声和篝火声等自然声音来创建沉浸式的环境音效。基于数字信号处理的知识，他有基础的音频混合功能和基于大型视觉语言模型（VLMs）的声音质量分析。

## ✨ 特点

- [x] 录制一个黑魂风格的篝火旁对白
- [x] 自己写一小段"旅人独白"，然后录音，加上篝火燃烧的背景音
- [x] 观鸟+冥想声音
- [x] 录一段"晨间森林"的声音，把鸟叫、流水、篝火燃烧的声音合成一个白噪音

## 📝 TODO List

- [ ] 好听的鸟叫
    - winter wren
    冬鸫，也叫雪鸫，是一种小型鸟类，体长约15厘米，体重约20克。它们通常生活在北方的针叶林和灌木丛中，以昆虫、种子和浆果为食。冬鸫的羽毛呈棕色或灰色，带有白色的腹部和尾巴。它们的叫声尖锐而响亮，常常在清晨和傍晚时分鸣叫。冬鸫是候鸟，冬季会迁徙到温暖的地区过冬。
    - 隐夜鸫 Hermit Thrush Catharus guttatus

    https://dongniao.net/nd/8730/%E9%9A%90%E5%A4%9C%E9%B8%AB/Hermit+Thrush/Hermit+Thrush

- [ ] 可以用 AI 语音合成，比如 ElevenLabs 来生成黑魂 NPC 风格的声音
- [ ] 用 AI 图片生成，比如 Midjourney 来生成一个关于"晨间森林"的图片
- [ ] 增加AI 诗朗诵？可以集成到UI里

## 🚀 快速上手

### 环境要求

```bash
pip install pydub librosa numpy scipy pillow openai matplotlib
```

### 基本用法

1. 生成白噪音混音（3分钟）：
```bash
python scripts/analyze_mix.py sounds/birds-forest-morning.mp3 sounds/indoor-hard-rain-sound.mp3 sounds/fireplace-with-crackling-sounds.mp3
```

2. 添加可选的鸟叫声：
```bash
python scripts/analyze_mix.py sounds/birds-forest-morning.mp3 sounds/indoor-hard-rain-sound.mp3 sounds/fireplace-with-crackling-sounds.mp3 voices/custom-bird-sound.mp3
```

3. 分析混音质量：
```bash
# 实时分析（推荐）
python scripts/analyze_with_vlm.py results/mix_MMDD_HHMM

# 禁用流式输出
python scripts/analyze_with_vlm.py results/mix_MMDD_HHMM --no-stream
```

## 📚 资源

### 声音来源

1. 免费音效：[Pixabay Birds Sound Effects](https://pixabay.com/sound-effects/search/birds/)

2. 鸟叫声数据库：
    - 发现了一个很厉害的网站：[Xenopy Bird Data](https://github.com/realzza/xenopy/tree/birdData)
    - 里面有各种鸟的叫声，可以用来做背景音, 可以自行上传，免费下载
    - 我上传了棕头鸦雀的叫声，效果还不错

3. 棕头鸦雀：
    - 太难找了，使用了b站的视频：[Bilibili Video](https://www.bilibili.com/video/BV1Fr421W7kE/)
    - 用这个浏览器插件录制了视频的音频，效果不错：chrome-extension@Chrome Audio Capture

4. 黑魂相关：
    - 伟大的防火女妈妈，睡前故事：[YouTube Video](https://www.youtube.com/watch?v=THLh8SxRw-8&ab_channel=Firekeeper)
    - 篝火音效：[Bonfire Dark Souls](https://www.myinstants.com/en/instant/bonfire-dark-souls-86656/)
    - my instant有很多音源，不过比较短：[My Instants Dark Souls](https://www.myinstants.com/en/search/?name=dark+souls)
    - 有人hack了黑魂的soundtrack，这里是800mb所有角色的语音条：[Reddit Post](https://www.reddit.com/r/opensouls3/comments/fm6pa3/all_dark_soul_3_npc_audio_files/)
    - 太多了暂时就没筛选，有兴趣的可以自己调试一下

## 🤝 参与贡献

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

## 📄 许可证

本项目采用 MIT 许可证开源。 