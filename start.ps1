
Start-Process cmd -ArgumentList "/k", "cd /d E:\Dev\FocusTrack\backend && venv\Scripts\activate.bat && python main.py"

Start-Process cmd -ArgumentList "/k", "cd /d E:\Dev\FocusTrack\frontend && npm run dev"