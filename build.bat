REM Install pyinstaller
pyinstaller --noconsole --onefile main.py --icon=icon.ico
REM Copy icon.ico to dist folder
copy icon.ico dist\icon.ico