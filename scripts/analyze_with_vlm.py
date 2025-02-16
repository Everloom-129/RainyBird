import os
import json
import base64
from typing import Dict, List, Optional
import argparse
from pathlib import Path
import requests
from PIL import Image
import io
from openai import OpenAI
import sys
from datetime import datetime

class VLMAnalyzer:
    def __init__(self, api_key: str):
        """Initialize VLM analyzer with API key.
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 string."""
        with Image.open(image_path) as img:
            # Resize if image is too large (max 2048x2048)
            if img.size[0] > 2048 or img.size[1] > 2048:
                img.thumbnail((2048, 2048))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
        return base64.b64encode(img_byte_arr).decode('utf-8')
        
    def analyze_results(self, result_dir: str, stream: bool = True) -> Dict:
        """Analyze results in the specified directory using GPT-4V.
        
        Args:
            result_dir: Path to results directory
            stream: Whether to stream the response
            
        Returns:
            Dictionary containing VLM analysis results
        """
        # Collect all analysis files
        result_path = Path(result_dir)
        metadata_files = list(result_path.glob("**/*_metadata.json"))
        noise_analysis_files = list(result_path.glob("**/*_noise_analysis.json"))
        analysis_images = list(result_path.glob("**/*_analysis.png"))
        noise_analysis_images = list(result_path.glob("**/*_noise_analysis.png"))
        
        summary = {
            "components": {},
            "final_mix": None
        }
        
        # Load metadata and analysis results
        for meta_file in metadata_files:
            component_name = meta_file.parent.name
            with open(meta_file) as f:
                metadata = json.load(f)
                
            # Find corresponding noise analysis
            noise_file = next((f for f in noise_analysis_files 
                             if f.stem.startswith(meta_file.stem)), None)
            if noise_file:
                with open(noise_file) as f:
                    noise_data = json.load(f)
            else:
                noise_data = {}
                
            # Find corresponding images
            analysis_img = next((str(f) for f in analysis_images 
                               if f.stem.startswith(meta_file.stem)), None)
            noise_img = next((str(f) for f in noise_analysis_images 
                            if f.stem.startswith(meta_file.stem)), None)
                
            component_data = {
                "metadata": metadata,
                "noise_analysis": noise_data,
                "analysis_image": analysis_img,
                "noise_analysis_image": noise_img
            }
            
            if component_name == "final_mix":
                summary["final_mix"] = component_data
            else:
                summary["components"][component_name] = component_data
        
        prompt = self._prepare_analysis_prompt(summary)
        
        images = []
        if summary["final_mix"]:
            if summary["final_mix"]["analysis_image"]:
                images.append({
                    "type": "analysis",
                    "path": summary["final_mix"]["analysis_image"]
                })
            if summary["final_mix"]["noise_analysis_image"]:
                images.append({
                    "type": "noise_analysis",
                    "path": summary["final_mix"]["noise_analysis_image"]
                })
        
        response = self._call_gpt4v(prompt, images, stream=stream)
        
        # Save analysis results to the result directory
        result_path = Path(result_dir)
        feedback_path = result_path / "vlm_feedback.md"
        
        # Create markdown content with timestamp
        markdown_content = f"""# 白噪音混音分析报告
> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 分析内容

{response}

## 技术指标

### 最终混音指标
```json
{json.dumps(summary["final_mix"]["noise_analysis"], indent=2, ensure_ascii=False)}
```

### 使用的音频文件
"""
        
        # Add component details
        for comp_name, comp_data in summary["components"].items():
            markdown_content += f"\n#### {comp_name}\n"
            markdown_content += f"- 文件名: {comp_data['metadata']['filename']}\n"
            markdown_content += f"- 时长: {comp_data['metadata']['duration']:.2f} 秒\n"
            markdown_content += f"- 采样率: {comp_data['metadata']['frame_rate']} Hz\n"
        
        # Save the markdown file
        with open(feedback_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print(f"\n分析报告已保存至: {feedback_path}")
        
        return {
            "summary": summary,
            "vlm_analysis": response
        }
    
    def _prepare_analysis_prompt(self, summary: Dict) -> str:
        """Prepare prompt for GPT-4V analysis."""
        # Get component names
        components = {
            "forest": "未知森林音频",
            "rain": "未知雨声音频",
            "fire": "未知篝火音频"
        }
        
        for comp_name, comp_data in summary["components"].items():
            if comp_data["metadata"].get("filename"):
                components[comp_name] = comp_data["metadata"]["filename"]

        prompt = f"""你好! 我是Tony, 一个热爱生活与音频处理的程序员。我正在为Holly, 一个可爱的，总是观鸟打黑魂画画的女孩，制作一个白噪音混音, 希望能帮助她在学习时保持专注。

我使用了以下几种声音元素：
- 森林环境声: {components['forest']}
- 雨声: {components['rain']}
- 篝火声: {components['fire']}
- 随机的鸟叫声（根据需要添加）

作为一个音频专家, 请你从专业和实用的角度分析这个混音：

1. 从白噪音的角度来看：
   - 频谱平坦度如何？(理想的白噪音应该在所有频率上能量分布均匀)
   - 声音的分布特性是否合适？(是否接近正态分布)
   - 自相关性如何？(对于学习场景来说是否合适)

2. 从实用性角度来看：
   - 各个声音元素的平衡是否恰当？
   - 频率分布是否适合长时间聆听？
   - 声音的时域特性是否自然？(不会让人感到突兀或不适)

3. 具体建议：
   - 作为学习背景音乐, 哪些地方可以改进？
   - 音量、混音比例等参数是否需要调整？
   - 是否存在可能影响专注力的问题？

以下是最终混音的一些关键指标：\n"""

        if summary["final_mix"]:
            noise_analysis = summary["final_mix"]["noise_analysis"]
            prompt += f"""
频谱平坦度: {noise_analysis.get('spectral_flatness', 'N/A')}
分布统计:
- 均值: {noise_analysis.get('distribution_analysis', {}).get('mean', 'N/A')}
- 标准差: {noise_analysis.get('distribution_analysis', {}).get('std', 'N/A')}
- 偏度: {noise_analysis.get('distribution_analysis', {}).get('skewness', 'N/A')}
- 峰度: {noise_analysis.get('distribution_analysis', {}).get('kurtosis', 'N/A')}

我提供了两种可视化分析：
1. 基础分析：显示波形和梅尔频谱图
2. 详细的噪音分析: 包括PSD(功率谱密度)、自相关性、分布直方图和STFT(短时傅里叶变换)

请帮我分析这些可视化结果和指标, 评估这个混音作为学习用的白噪音是否合适, 以及具体有什么可以改进的地方。

特别关注：
1. 声音是否会分散注意力？
2. 长时间听是否舒适？
3. 是否真的能帮助专注？

如果有改进建议, 请尽量具体一些, 比如具体的音量调整比例或频率范围的建议。谢谢！"""

        return prompt
    
    def _call_gpt4v(self, prompt: str, images: List[Dict], stream: bool = True) -> str:
        """Call GPT-4V API with prompt and images.
        
        Args:
            prompt: Text prompt for analysis
            images: List of image paths to analyze
            stream: Whether to stream the response
            
        Returns:
            Analysis response from GPT-4V
        """
        # Prepare messages with images
        content = [{"type": "text", "text": prompt}]
        
        # Add images to content
        for img in images:
            print(img["path"])
            base64_image = self.encode_image(img["path"])
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                }
            })
        
        try:
            # Create completion with streaming
            response = self.client.chat.completions.create(
                model="chatgpt-4o-latest",
                messages=[{
                    "role": "user",
                    "content": content
                }],
                max_tokens=4096,
                stream=stream
            )
            
            if stream:
                # Handle streaming response
                collected_messages = []
                print("\nReceiving analysis (streaming):")
                print("-" * 50)
                
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        collected_messages.append(content)
                
                print("\n" + "-" * 50)
                return "".join(collected_messages)
            else:
                # Handle regular response
                return response.choices[0].message.content
                
        except Exception as e:
            error_msg = f"Error calling GPT-4V API: {str(e)}"
            print(error_msg, file=sys.stderr)
            return error_msg


def main():
    parser = argparse.ArgumentParser(description="Analyze audio mix results using VLM")
    parser.add_argument("result_dir", help="Directory containing analysis results")
    parser.add_argument("--output", help="Output file for analysis results")
    parser.add_argument("--no-stream", action="store_true", help="Disable response streaming")
    
    args = parser.parse_args()
    api_key = open("configs/api.key").read().strip()
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
        
    analyzer = VLMAnalyzer(api_key)
    results = analyzer.analyze_results(args.result_dir, stream=not args.no_stream)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
    elif not args.no_stream:
        # Results already printed during streaming
        pass
    else:
        print("\nVLM Analysis Results:")
        print("-" * 50)
        print(results["vlm_analysis"])

if __name__ == "__main__":
    main() 