# videoAI-generate

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white" alt="Google Colab">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/Machine_Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="ML">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/last-commit/Lswitch18/videoAI-generate/main?style=for-the-badge" alt="Last Commit">
</p>

---

## 動画生成 - AI Video Generation with Open Source

This project provides open-source tools for AI-powered video generation using **Tencent Hunyuan** model, running on **Google Colab**.

---

## 🎥 Features

- **AI Video Generation**: Generate videos from text prompts using Hunyuan model
- **Image to Video**: Transform static images into dynamic videos
- **Multi-modal**: Support for text-to-video and image-to-video
- **Free to Use**: Runs on Google Colab free tier
- **Open Source**: All code is available and modifiable

---

## 🚀 Getting Started

### Prerequisites
- Google Account (for Colab)
- HuggingFace account (for model access)

### Installation

```bash
# Clone the repository
git clone https://github.com/Lswitch18/videoAI-generate.git
cd videoAI-generate

# Install dependencies
pip install -r requirements.txt
```

### Running on Google Colab

1. Open `install_hunyuan.sh` in Google Colab
2. Run the installation cells
3. Use `brain_hunyuan.py` or `gerar_video.py` to generate videos

### Quick Example

```python
from brain_hunyuan import generate_video

# Generate video from prompt
video_path = generate_video(
    prompt="A beautiful sunset over the ocean with waves",
    duration=5,
    fps=30
)

print(f"Video saved to: {video_path}")
```

---

## 📁 Project Structure

```
videoAI-generate/
├── brain.py              # Main brain module
├── brain_hunyuan.py     # Hunyuan integration
├── gerar_video.py       # Video generation script
├── install_hunyuan.sh  # Colab installation script
├── requirements.txt    # Python dependencies
├── agent.md          # Agent configuration
├── README.md         # This file
└── docs/            # Additional documentation
```

---

## 🛠️ Tech Stack

| Technology | Description |
|------------|------------|
| Python 3.x | Programming language |
| Hunyuan | Tencent video generation model |
| OpenCV | Video processing |
| Google Colab | Free cloud computing |
| PyTorch | Deep learning framework |

---

## 📖 Documentation

- [Installation Guide](./instalacao_hunyuan_video_colab.md) - Step by step installation
- [Agent Configuration](./agent.md) - Agent settings
- [Video Generation](./gerar_video.py) - Usage examples

---

## ⚠️ Important Notes

1. **Rate Limits**: Google Colab has usage limits on free tier
2. **Model Download**: First run downloads the model (~GB of storage)
3. **GPU Queue**: May need to wait for GPU availability on Colab

---

## 🤝 Contributing

1. Fork the repository
2. Create your branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit your changes (`git commit -m 'feat: nova funcionalidade'`)
4. Push to branch (`git push origin feature/nova-funcionalidade`)
5. Open a Pull Request

---

## 📜 License

MIT License - Copyright (c) 2024

---

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

<p align="center">
  <sub>Feito com ☕ edeterminação</sub>
  <br>
  <a href="https://github.com/Lswitch18">
    <img src="https://img.shields.io/badge/-lswitch18-black?style=flat&logo=github" alt="lswitch18">
  </a>
</p>