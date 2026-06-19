Earth's Magnetic Shield: Shock Detectives

This is a data-driven Solar Wind Shock Wave Automated Diagnostics Dashboard built entirely with Python, Streamlit, and OpenCV.

The Backstory & Inspiration
This project is inspired by the citizen science project [Shock Detectives](https://www.zooniverse.org/projects/michielfr/shock-detectives) on Zooniverse. While browsing their platform, 
I realized that volunteers spend countless hours visually classifying these complex solar wind shock waves. As a high school tech enthusiast, I thought: *“Wait, why not write an algorithm 
to automate this and see if pure math and geometry can back up human eyes?”* So, I spent my nights building this app to replace subjective guesswork with rock-solid pixel statistics! 

What it Does (Key Features)
- 100% Code-Driven Analysis**: No more guessing. The app scans every pixel of the telemetry images to detect the real state of shock waves (Peaceful vs. Chaotic).
- Anti-Aliasing Shield**: Real world data is messy! I designed a custom cropping and thresholding pipeline that ignores chart borders, labels, and even the annoying "grey-scale noise" left behind by anti-aliasing artifacts. 
- Regional Micro-Feature Dive**: The algorithm slices the spectrogram into 5 precise columns (Regions A to E). It then runs separate CV detection models on the Energy Spectrogram, Time-series Lines, and the Fluctuation Ridge simultaneously.
- Global Architecture Mapping**: It automatically gathers all the clues from Regions A-E and gives a definitive final boss verdict: Is the solar wind *Fully Chaotic*, *Fully Peaceful*, or a *Mixed* hybrid state?
- 8-Language Internationalization**: Zero-dependency UI language toggling! Fully supports English, 简体中文, 繁體中文, Español, Français, Deutsch, Русский, and 한국어.
- Foolproof Container Logic**: Enforces a strict single-file upload rule to protect the backend pipeline from crashing when users accidentally spam files.

How to Run it Locally
1. Clone this repo:
```bash
git clone [https://github.com/CS3AI/shock-detectives.git](https://github.com/CS3AI/shock-detectives.git)
cd shock-detectives
