# Computer Vision and Generative AI-Based Code Generation System

## 📌 Overview
This project presents a hybrid AI system that automates the process of converting UI screenshots into HTML/CSS/JS code. It combines classical computer vision techniques for layout detection with a fine-tuned large language model (Mistral-7B) to generate clean, structured frontend code.

## 🎓 Course Info
- **Course:** CSC-528: Computer Vision  
- **University:** DePaul University  
- **Quarter:** Spring 2025  

## 👨‍💻 Team Members
- Arul Michael Antony Felix Raja — afelixra@depaul.edu  
- Vasanthkumar Ramamoorthi — vramamoo@depaul.edu  
- Akash Sampath — asampath@depaul.edu  

## 🧠 Problem Statement
Frontend developers often spend hours manually translating design mockups into code. This project solves that by building a two-stage AI pipeline:
1. **Computer Vision:** Extracts layout structure using grayscale conversion and Canny edge detection.
2. **LLM Code Generation:** A fine-tuned Mistral-7B model generates HTML code from the visual features.

## 🛠️ Tech Stack
- Python 3.12
- OpenCV
- Mistral-7B (via QLoRA fine-tuning)
- Hugging Face Datasets (WebSight & Fluent-Dev)
- PyTorch
- FastAPI (optionally for web interface)

## 🧪 Project Structure
- `src/` — All Python modules including CV + LLM pipeline
- `samples/` — Evaluation and ablation data
- `web_outputs/` — Generated HTML code samples
- `web_uploads/` — Input UI screenshots
- `presentation/` — Final report and slides
- `requirements.txt`, `Makefile`, and `pyproject.toml` for dependencies and setup

## 🚀 How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run code generation from image
python main.py --input path/to/ui_image.png
```

## 📝 Final Deliverables
- ✅ Source Code  
- ✅ Research Report (PDF)  
- ✅ Presentation (PPTX)  
- ✅ Sample HTML Outputs

## 📈 Results
The model was trained over 3 epochs using QLoRA. Loss reduced from `2.9` to `1.2`, generating clean, structure-preserving HTML aligned with the UI layout.

---

**Note:** For demonstration purposes only. The Mistral-7B model was fine-tuned on a subset due to hardware limits.

---