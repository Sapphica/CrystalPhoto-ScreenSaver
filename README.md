
# CrystalPhoto-ScreenSaver
*A modern Python/PyGame photo screensaver engine built to replace the sluggish, limited, and non-random Windows screensaver.*

<div align="center">

![Platform](https://img.shields.io/badge/PLATFORM-WINDOWS-444444?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/PYTHON-3.x-306998?style=for-the-badge&logo=python)
![PyGame](https://img.shields.io/badge/PYGAME-ENGINE-004f7c?style=for-the-badge)
![Build](https://img.shields.io/badge/BUILD-STABLE-8A2BE2?style=for-the-badge)
![Mode](https://img.shields.io/badge/TYPE-SCREENSAVER-9370DB?style=for-the-badge)

</div>

---

## ✨ Purpose
The default Windows photo screensaver is slow, non-random, handles iPhone photos poorly, and takes too long to return to the desktop.

CrystalPhoto-ScreenSaver fixes all of this with a real rendering engine:
- True randomness (deck shuffle)
- Smooth transitions
- Instant return-to-desktop
- Correct iPhone portrait scaling
- HEIC/HEIF support
- Multi-monitor stability

---

## ⚙️ Features
- Genuine random sequencing (no repeats until cycle ends)
- Smooth transitions (fade, slide, crossfade, checkerboard, blocky dissolve)
- Weighted transition system (fade = 50%)
- Instant desktop return via non-blocking event loop
- HEIC/HEIF loading via pillow_heif
- EXIF orientation correction
- Smart image scaling (landscape fill, portrait fit)
- Multi-monitor compatible rendering
- Recursive folder scanning
- Supports `/s`, `/p`, `/c` Windows screensaver arguments
- Packaged with PyInstaller → rename exe to .scr

---

## 🧠 Tech Stack
- Python 3.x  
- PyGame for rendering + animation  
- Pillow + pillow_heif for decoding images  
- PyInstaller for deployment  
- Windows screensaver protocol behavior  

---

## 🚀 Usage

Run fullscreen screensaver:
python screensaver.py /s

Preview mode:
python screensaver.py /p

Config dialog placeholder:
python screensaver.py /c

---

## 🏁 Build Into a Windows Screensaver

1. Build with PyInstaller:
pyinstaller --noconsole --onefile screensaver.py

2. Rename the output file:
screensaver.exe → CrystalPhoto-ScreenSaver.scr

3. Move it into the system directory:
C:\Windows\System32

4. Select it from Windows screensaver settings.
Done.

---

## 🧩 Recruiter-Ready Summary
CrystalPhoto-ScreenSaver is a custom-built fullscreen rendering system designed to replace the default Windows photo screensaver. It provides high-performance image transitions, true randomness, correct EXIF handling, iPhone-photo scaling, and instant exit responsiveness.

This project demonstrates:
- Rendering pipeline architecture
- Transition animation engine design
- Image decoding, EXIF correction, HEIC parsing
- Real-time event-loop control
- System-level Windows integration
- Python-to-binary packaging (PyInstaller)

---

# 🛠 Technical Architecture

## 1. Image Pipeline
- Recursive folder scan  
- Filters junk files (.DS_Store, Thumbs.db, macOS "._" files)  
- Accepts JPG, PNG, BMP, GIF, HEIC  
- Registers HEIC opener  
- Applies EXIF orientation (3/6/8)  
- Converts image to RGB/A when required  
- Creates PyGame surfaces via frombuffer  
- Yields (surface, filename) pairs for logging  

---

## 2. Random Deck System
Implements a true shuffle deck:
- Build list of all images
- Shuffle once
- Pop items one by one
- When empty → reshuffle entire deck

Advantages over Windows screensaver:
- No loops or repeats
- Every image shown before repeat
- True randomness, no hidden weighting

---

## 3. Transition Engine
Modular transition structure:
- fade  
- slide  
- crossfade  
- checkerboard  
- blocky dissolve  

Weighted system:
- Fade used 50% of the time (best overall look)
- Others at 12.5% each

Transitions run at 30–60 FPS depending on effect.

---

## 4. Scaling Engine

For very large images (≥ 4K):
- Landscape: scale to fill
- Portrait: scale to fit

For normal photos:
- Scale up to 75% of screen size
- Maintains aesthetic spacing
- Prevents giant portrait dominance

---

## 5. Exit Handling
Every single frame checks:
- Keyboard input
- Mouse movement
- Mouse clicks
- QUIT events

Exit sequence:
pygame.mouse.set_visible(True)
pygame.quit()
sys.exit()

This ensures instant shutdown unlike Windows’ sluggish default screensaver.

---

## 6. Interruptible Wait Timer
Instead of a sleep:
- 60 FPS loop
- Each frame accumulates elapsed time
- Each frame checks for exit events

Gives:
- Instant exit  
- Smooth timing  
- No freeze-on-wait behavior  

---

## 7. Windows Screensaver Arguments
CrystalPhoto supports:
- /s — Start screensaver mode  
- /p — Preview mode (not implemented but handled)  
- /c — Config dialog  

Matches native Windows .scr behavior.

---

## 🔧 PyInstaller Packaging Details
- Audio disabled with SDL_AUDIODRIVER=dummy  
- Single-file binary  
- No console window  
- Rename exe → .scr to integrate into Windows  

---

# 🔮 Roadmap
- GPU shader transitions (moderngl)
- Ken Burns motion effect
- JSON/INI config profile
- Per-monitor tuning
- CrystalSuite unified experience integration

---

## ❤️ Author
Created by **Sapphica**  
Senior Firmware QA Automation Engineer • Embedded Systems • Graphics/UI Pipeline Engineer  
Creator of the **CrystalSuite** ecosystem (CrystalLCD, CrystalPhoto, JinxLED Engine, and more)
```
