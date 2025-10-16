TikTok AI Mobile Lite
=====================

This project builds a lightweight Android app (Kivy) that generates short videos locally without heavy ML models.
It uses template-based script generation, gTTS for Portuguese TTS, pillow to create images with text, and moviepy to assemble the video.

How to use:
1. Extract the repo and push to GitHub (branch main).
2. Optional: test locally on desktop: `python3 tiktok_ai_mobile_pro/main.py` (requires dependencies).
3. Configure GitHub Actions (workflow provided) or build locally with Buildozer/Termux.
4. Install APK produced by workflow on your Android phone.
