import os
PROJECT_DIR = "tiktok_ai_mobile_pro"
os.makedirs(PROJECT_DIR, exist_ok=True)
spec = r"""[app]
title = TikTok AI Mobile Lite
package.name = tiktokailite
package.domain = org.ludeluda
source.dir = .
source.include_exts = py,png,jpg,kv,db
version = 1.0
requirements = python3,kivy,requests,pillow,moviepy,pydub,gTTS
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
"""
with open(os.path.join(PROJECT_DIR, 'buildozer.spec'), 'w') as f:
    f.write(spec)
print('Created buildozer.spec at', os.path.join(PROJECT_DIR, 'buildozer.spec'))
