@echo off
echo Starting Library Dashboard System...

:: Start Backend
start "Library Backend" /D "C:\Users\PC\.gemini\antigravity\brain\36954c62-9d67-4848-94a4-278b6cac4051" python backend.py

:: Start Frontend
cd "C:\Users\PC\.gemini\antigravity\brain\36954c62-9d67-4848-94a4-278b6cac4051\dashboard"
npm run dev
