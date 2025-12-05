
"C:\Python Projects\screen_saver\.venv\Scripts\python.exe" -m PyInstaller ^
  screen_saver.py ^
  --noconsole ^
  --onefile ^
  --icon=linux.ico ^
  --name=Shawna_Screen_Saver ^
  --hidden-import=pygame ^
  --hidden-import=pygame._sdl2 ^
  --hidden-import=pygame.freetype ^
  --hidden-import=PIL ^
  --hidden-import=pillow_heif

REM Rename to .scr
rename "dist\Shawna_Screen_Saver.exe" "Shawna's Screen Saver.scr"

echo Build complete: dist\Shawna's Screen Saver.scr

REM Clean old build/dist
rmdir /s /q build

pause