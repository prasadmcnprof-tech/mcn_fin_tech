@echo off
cd /d %~dp0
echo ============================================
echo Starting Finance Complaince Web Application
echo ============================================
call venv\Scripts\activate
python manage.py check
python manage.py migrate
start http://127.0.0.1:8000
python manage.py runserver
pause
